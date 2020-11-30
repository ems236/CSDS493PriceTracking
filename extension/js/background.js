// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';


// Using chrome.identity
var manifest = chrome.runtime.getManifest();

var clientId = encodeURIComponent(manifest.oauth2.client_id);
var scopes = encodeURIComponent(manifest.oauth2.scopes.join(' '));
var redirectUri = encodeURIComponent('https://' + chrome.runtime.id + '.chromiumapp.org/');
var state = encodeURIComponent('meet' + Math.random().toString(36).substring(2, 15));
var nonce = encodeURIComponent(Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15));
var prompt = encodeURIComponent('consent');

var url = 'https://accounts.google.com/o/oauth2/v2/auth' + 
          '?client_id=' + clientId + 
          '&response_type=id_token' + 
          '&access_type=offline' + 
          '&redirect_uri=' + redirectUri + 
          '&scope=' + scopes +
          '&nonce=' + nonce +
          '&state=' + state +
          '&prompt' + prompt

console.log("gothere");
console.log(url);

//You essentially have to sacrifice a child to sundar pichai to obtain an id token
//This actually seems to work though
//see https://medium.com/swlh/oauth2-openid-chrome-extension-login-system-29285323882f  
// and https://stackoverflow.com/questions/26256179/is-it-possible-to-get-an-id-token-with-chrome-app-indentity-api/32548057#32548057

console.log("adding listener")

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("got message");
  if (request.message === 'login') {
    chrome.identity.launchWebAuthFlow(
    {
        'url': url, 
        'interactive':true
    }, 
    function(redirect_url) {
        console.log(redirect_url);
        if (chrome.runtime.lastError) {
            console.log(chrome.runtime.lastError.message);
            sendResponse({"success": false})
        }
        else {
            let id_token = redirect_url.substring(redirect_url.indexOf('id_token=') + 9);
            id_token = id_token.substring(0, id_token.indexOf('&'));
            console.log(id_token);
            sendResponse({"success": true, "token": id_token});
            console.log(redirect_url);
        }
    }
  );

    return true;
  }
});

  chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: '#3aa757'}, function() {
      console.log('The color is green.');
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'www.amazon.com'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });


  // Listen for notification messages 
  chrome.runtime.onMessage.addListener(data => {
    if (data.type === 'notification') {
      var notification = chrome.notifications
      notification.create('', data.options);
    }
  });
