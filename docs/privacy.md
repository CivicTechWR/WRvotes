---
title: Privacy 
layout: page
readable-widths: true
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

- We respect the [Global Privacy
  Control](https://globalprivacycontrol.org/) standard. Many browsers
  have support for this standard built-in, except for Google Chrome.
  On that browser, there are some extensions such as [Privacy
  Badger](https://privacybadger.org/) which provide Global Privacy
  Control functionality.

- We respect the [Do Not
  Track](https://en.wikipedia.org/wiki/Do_Not_Track) header. This is
  considered deprecated but 
  still supported in [many web
  browsers](https://developer.mozilla.org/en-US/docs/Web/API/navigator/doNotTrack).

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

A more extreme solution is to disable JavaScript. This will break the
following: 

- The front-page map will not work.
- Some JavaScript is used to hide and expand content. This content
  will be expanded without JavaScript.
- Favouriting candidates will not work. Notes you make about
  candidates will disappear if you close the page.

However, all of the site content should remain accessible.


Local Storage and Cookies
-------------------------

Some functionality (such as favouriting candidates) uses JavaScript
[Local Storage](https://en.wikipedia.org/wiki/Web_storage) to remember
your selections when you close your browser. This information is never
transmitted over the Internet. 

You can clear the notes and favourites you have made by clearing your
local storage. [CLICK HERE?]


Third-Party Services
--------------------

We host this website on GitHub Pages. They [collect server logs for
security
purposes](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#data-collection).
As far as we know we have no access to these logs. 

We use OpenStreetMap for the front page map. They also [collect logs
and some user
data](https://wiki.osmfoundation.org/wiki/Privacy_Policy#Data_we_receive_automatically).
