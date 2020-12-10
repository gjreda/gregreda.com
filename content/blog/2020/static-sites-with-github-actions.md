title: Deploying static sites with Github Actions
date: 2020-12-09
slug: deploying-static-sites-with-github-actions
tags: pelican, github

A while back I [wrote](http://gregreda.com/2015/03/26/static-site-deployments/) about deploying my site using Github and Travis CI. But recently it seems [Travis CI stopped being free for open source projects](https://news.ycombinator.com/item?id=25338983).

If you're using a static site generator for your site and hosting it on it on S3, you can use [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) to build and deploy your site on each commit (or PR, or whatever).

## Setup

If you've already set up Travis CI to deploy your static site to S3, switching to Github Actions won't be very difficult.

Actions are defined in YAML and need to live at a path of `.github/workflows` within your repo. We'll name ours `deploy.yml`, so its path will be `.github/workflows/deploy.yml`.

Before defining our workflow steps, we'll want to add any necessary secret passwords, keys, tokens, and such to our repo's [encryped secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets). This will allow them to be accessed by the workflow, but securely stored and only visible to those with access to the repo.

Since my site is hosted using S3 and Cloudfront, I'll need secrets for my AWS access keys.

![My repo's Github Secrets page](/images/github-secrets.png)

Next, we'll create our `deploy.yml` file. Github kindly supplies [starter workflows](https://github.com/actions/starter-workflows) in many languages, but since this site uses Pelican, a static site generator for Python, we'll use the [Python starter workflow](https://docs.github.com/en/free-pro-team@latest/actions/guides/building-and-testing-python).

```yaml
name: deploy
on:
  push:
    branches: [master]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '2.7'
```
Yes, I'm still using a very old version of Pelican with Python 2.7. I swear I use Python3 everywhere else.

Since we're deploying to S3, we'll need to add a step for configuring our AWS credentials using the [configure credentials action](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions). The `aws-region` should match whichever region your bucket is in.

```yaml
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with: 
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
```

Because my website's repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), I need to add another step for checking out and updating these submodules on each build.

```yaml
    - name: Build submodules
      run: |
        sed -i 's/git@github.com:/https:\/\/github.com\//' .gitmodules
        git submodule update --init --recursive
```

We also need to `pip install` any dependencies from `requirements.txt`, like Pelican.

```yaml
    - name: Install dependencies
      run: |
        sudo apt-get install -qq pandoc
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```

And finally, we can build our site, deploy it to S3, and invalidate the Cloudfront cache.

```yaml
    - name: Build website
      run: |
        pelican content
    - name: Deploy to S3
      run: |
        aws s3 sync output/. s3://www.gregreda.com --acl public-read
    - name: Invalidate Cloudfront cache
      run: |
        aws configure set preview.cloudfront true
        aws cloudfront create-invalidation --distribution-id ${{ secrets.AWS_CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
```
Putting it all together gives us [this YAML file](https://github.com/gjreda/gregreda.com/blob/master/.github/workflows/deploy.yml), which builds and deploys this website on every commit to `master`.

That's it. Continuous deployment for your S3 hosted website.