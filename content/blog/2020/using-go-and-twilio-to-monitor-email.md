title: Using Go and Twilio to monitor my email
slug: using-go-and-twilio-to-monitor-my-email
date: 2020-12-11
tags: go
description: Sometimes I'm anticipating an email and want to be notified as soon as I receive it, but I don't want to stare at my inbox or use push notifications. Here's how I solved that problem using Go and Twilio.

Sometimes I'm expecting an email and want to be notified shortly after receiving it. But I also don't want to stare at my inbox, something I don't particularly enjoy checking in the first place.

To illustrate an example, imagine you're browsing a niche site with limited edition goods, some of which you love but are out of stock (they're limited, after all). Each item has a helpful "Join waitlist" button, allowing you to provide your email address and receive an email once the item is back in stock. Great feature!

There are a couple key pieces to the above scenario though:

1. The items are limited (supply).
2. There's a waitlist of unknown size (demand).

In effect, we are being told that supply is fixed and demand is not. If demand is far greater than supply it's likely the item will go out of stock again shortly after the email goes out. This is because those who receive the email first will rush to purchase it, knowing that it's a limited item. How can you ensure you see the email shortly after it's sent?

One idea is to just turn on push notifications for all email, but this approach would have a lot of noise and little signal. I'd like to be notified when a _specific_ email arrives, not when _any_ email arrives.

I spend a lot of time in the Messages app texting with friends and family, so a service that sends me a text message would be great, since I'd see it sooner than an email.

Knowing [Gmail has an API](https://developers.google.com/gmail/api) and [Twilio](https://www.twilio.com/referral/XCX3Mu) would make the text messaging piece easy, this felt like a fun little problem to solve and a good excuse to try a new programming language. I opted for [Go](https://golang.org/).

## Why Go

I've primarily worked in [Python](https://www.python.org/) for the last decade. It's a language that I know and love deeply, and I especially appreciate its emphasis on readability and simplicity. It's a language that allows me to focus on the problem I am solving and doesn't get in the way.

But two common complaints that many Python users eventually have are the language's lack of static typing and that it is slow. While I've rarely found performance to truly be a bottleneck, I have gained an appreciation for statically typed, compiled languages.

Go was born at a time when Python adoption was on the rise thanks to the above qualities. While languages like Java and C++ allowed for more performant solutions, each came with more verbosity and complexity.

Go was designed with developer productivity as a primary concern. One of its creators, Rob Pike, [describes it best](https://commandcenter.blogspot.com/2012/06/less-is-exponentially-more.html):

> What you're given is a set of powerful but easy to understand, easy to use building blocks from which you can assemble—compose—a solution to your problem. It might not end up quite as fast or as sophisticated or as ideologically motivated as the solution you'd write in some of those other languages, but it'll almost certainly be easier to write, easier to read, easier to understand, easier to maintain, and maybe safer.

> To put it another way, oversimplifying of course:

> Python and Ruby programmers come to Go because they don't have to surrender much expressiveness, but gain performance and get to play with concurrency.

This philosophy feels very [Pythonic](https://stackoverflow.com/a/25011492/1419514) to me. It's the reason I opted to give Go a ... uh, go.

## Code

A Google search of "golang gmail" brings up a [quickstart](https://developers.google.com/gmail/api/quickstart/go) on using the Gmail API and Go to read your inbox labels. The vast majority of this code is authentication handling but it's also almost everything we need.

To search our inbox and send a text when the search has results, we'll add the following functions to the quickstart code:

1. `queryMessages`, which will call Gmail's [`user.messages.list`](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list) method to search a user's inbox and return any matching messages. 
2. `buildSMS`, which will create the message content to be sent via text/SMS message.
3. `sendSMS`, which will use the [Twilio REST API](https://www.twilio.com/docs/usage/api) to send the text message to a given phone number.

#### queryMessages

1. Takes inputs of a [Gmail Service object](https://pkg.go.dev/google.golang.org/api/gmail/v1#Service), a string denoting the user, and another string for the search `q` (e.g. "foo", "from:foo", etc.). Note the `*` symbol preceeding a type indicates it is a [pointer](https://en.wikipedia.org/wiki/Pointer_(computer_programming)). Go allows for objects to be passed by reference, differing from Python's "[pass by assignment](https://docs.python.org/3/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference)".
2. Using the `service` pointer, calls the Gmail's `list` endpoint using the `q` parameter to find any messages matching the search. This is akin to using the search box within Gmail.
3. Does some logging and checks to ensure the API returns a valid response.
4. Returns an array of [`Message`](https://pkg.go.dev/google.golang.org/api/gmail/v1#Message) pointers.

```go
func queryMessages(service *gmail.Service, user string, q string) []*gmail.Message {
	log.Printf("Searching for messages containing: %v", q)
	response, err := service.Users.Messages.List(user).Q(q).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve messages: %v", err)
	}
	if response.HTTPStatusCode != 200 {
		log.Printf("Request returned status code: %v\n", response.HTTPStatusCode)
	}
	log.Printf("Number of messages found: %v\n", len(response.Messages))
	return response.Messages
}
```

#### buildSMS

`buildSMS` takes many of the same inputs as the previous function (there's definitely a nicer way to write this code), but also takes in the list of `Messages` the previous function returned, as well as whether each `Message` snippet should be included in the SMS message.

```go
func buildSMS(service *gmail.Service, user string, messages []*gmail.Message, q string, includeSnippets bool) string {
	var sb strings.Builder
	fmt.Fprintf(&sb, "Hi! You have %v emails matching your search of \"%v\".", len(messages), q)
	if len(messages) == 0 {
		return ""
	}
	if includeSnippets == true {
		fmt.Fprintf(&sb, " Here's what they look like.\n")
		for i, m := range messages {
			fmt.Printf("(%v) Fetching message %v\n", i+1, m.Id)
			m, err := service.Users.Messages.Get(user, m.Id).Do()
			if err != nil {
				log.Fatalf("Unable to retrieve message ID %v: %v", m.Id, err)
			}
			fmt.Fprintf(&sb, "(%v) - %v\n", i+1, m.Snippet)
		}
	}
	return sb.String()
}
```

Go's [`strings.Builder`](https://golang.org/pkg/strings/#Builder) creates an object in memory which allows strings to be written directly to it, thus minimizing any memory copying. When declaring `var sb strings.Builder` we're getting a block in the memory registry and then writing directly to it with each `Fprintf` to `&sb`. Calling `sb.String()` returns a string of whatever we've written to the `Builder`.

#### sendSMS

Finally, we need to call the [Twilio SMS API](https://www.twilio.com/docs/sms) to send our text. All that's needed is sending an POST request to the `/Messages.json` endpoint with our message data encoded as json.

```go
func sendSMS(phoneNumber string, message string, config *Config) {
	msgData := url.Values{}
	msgData.Set("To", phoneNumber)
	msgData.Set("From", config.Twilio.PhoneNumber)
	msgData.Set("Body", message)
	reader := *strings.NewReader(msgData.Encode())

	reqURL := config.Twilio.BaseURL + "/Accounts/" + config.Twilio.AccountSID + "/Messages.json"

	client := &http.Client{}
	req, _ := http.NewRequest("POST", reqURL, &reader)
	req.SetBasicAuth(config.Twilio.AccountSID, config.Twilio.AuthToken)
	req.Header.Add("Accept", "application/json")
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	response, _ := client.Do(req)
	var data map[string]interface{}
	decoder := json.NewDecoder(response.Body)
	err := decoder.Decode(&data)

	if response.StatusCode >= 200 && response.StatusCode < 300 {
		if err == nil {
			log.Printf("Twilio message SID: %v", data["sid"])
		}
	} else {
		log.Printf("Twilio returned status: %v", response.Status)
	}
}
```

#### Putting it all together
Putting all the necessary pieces together gives us [this script](https://github.com/gjreda/gmail-text-notifications/blob/master/main.go), which takes an input search term(s) and phone number.

```
$ go build main.go
$ ./main -q hello -phone +131255555555

2020/12/09 16:28:20 Searching for messages containing: hello
2020/12/09 16:28:21 Number of messages found: 100
2020/12/09 16:28:22 Twilio message SID: SM72f7e0080030412284dec3afab19489d
```

<center>
<img src="/images/email-sms-message.jpg" alt="SMS letting me know I have emails matching the search" width="350px">
</center>
I found Go pretty nice to work with and intend to explore it more. It scratches the "statically typed, compiled language" itch I've had recently. I'm particularly intrigued by its concurrency patterns and plan to do some comparisons against Python + pandas for data pipeline tasks.

You can find the code for this project [on my Github](https://github.com/gjreda/gmail-text-notifications).

**Additional Reading:**

- [the asterisk and the ampersand - a golang tale](https://winterflower.github.io/2017/08/20/the-asterisk-and-the-ampersand/)
- [Less is exponentially more](https://commandcenter.blogspot.com/2012/06/less-is-exponentially-more.html)