#useful for building jekyll locally to test before deploying
#to github-pages

FROM starefossen/ruby-node:2-6-alpine

ENV GITHUB_GEM_VERSION 179
ENV JSON_GEM_VERSION 1.8.6

RUN apk --update add --virtual build_deps \
    build-base ruby-dev libc-dev linux-headers \
    curl libcurl

RUN mkdir -p /usr/src/app
RUN mkdir -p /_site

WORKDIR /usr/src/app

COPY Gemfile /usr/src/app/Gemfile
COPY Gemfile.lock /usr/src/app/Gemfile.lock

RUN bundle install

COPY . /usr/src/app

RUN ./build_site

EXPOSE 4000 80
 
WORKDIR /usr/src/app/docs

CMD jekyll serve -d /usr/src/app/_site -H 0.0.0.0 -P 4000
