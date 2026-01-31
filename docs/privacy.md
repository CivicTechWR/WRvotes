---
title: Privacy 
layout: page
---

Privacy
=======

This website attempts to respect your privacy while still gathering
some aggregate information.

We would like to evaluate how useful the site is to people, and to
generate talking points we can use when promoting the project to
others (for example: "Our project got X number of views the week
before the election.")

We would like to answer the following kinds of questions:

- Roughly how many people used our site?
- Which wards had the most engagement?
- Which resources did people find most useful? Meeting recordings?
  Candidate websites? Opinion pieces? Something else?

We do not have advertising or other monetization on the site. 
We do not intentionally share individualized data with third parties. 

Google Analytics and Google Tag Manager
---------------------------------------

Somewhat reluctantly, we use Google Analytics 4 to track website
usage. You can read its [privacy policy
here](https://support.google.com/tagmanager/answer/9323295?hl=en). To enhance privacy, we have taken the following steps:

- We respect the [Do Not
  Track](https://en.wikipedia.org/wiki/Do_Not_Track) header. This is
  considered deprecated but 
  still supported in [many web
  browsers](https://developer.mozilla.org/en-US/docs/Web/API/navigator/doNotTrack).
  It appears that there is a replacement standard called [Global
  Privacy Control](https://globalprivacycontrol.org/) that is in
  development, but as of October 2022 nobody supports it yet. 

- We have disabled local cookie storage for Google Tag Manager.
  This means we can [no longer track unique
  visitors](https://helgeklein.com/blog/google-analytics-cookieless-tracking-without-gdpr-consent/) effectively. 
  Oh well.

- We have requested that Google Analytics/Tag Manager anonymize IP
  addresses.

You can see how we call Google Analytics/Tag Manager [in the source
code](https://github.com/CivicTechWR/{{ site.repository_name }}/blob/master/docs/_includes/google-analytics.html). 

Many ad blocking plugins (such as [UBlock
Origin](https://ublockorigin.com/)) will block Google Analytics and
Google Tag Manager automatically. 

A more extreme solution is to
disable JavaScript, which will break the front-page map but not affect
the rest of the website dramatically.


Third-Party Services
--------------------

We host this website on GitHub Pages. They [collect server logs for
security
purposes](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#data-collection).
As far as we know we have no access to these logs. 

We use OpenStreetMap for the front page map. They also [collect logs
and some user
data](https://wiki.osmfoundation.org/wiki/Privacy_Policy#Data_we_receive_automatically).
