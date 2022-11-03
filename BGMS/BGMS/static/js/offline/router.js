/* jshint esversion:6 */

class Router {

  constructor() {
    this.routes = {
      GET: {},
      POST: {},
      PUT: {},
      PATCH: {},
      DELETE: {},
      all: {},
      default: (request) => {
        return self.fetch(request);
      },
    };
  }

  /**
   * Finds the correct handler, falling back to the default if needed
   * QUESTION: Should ALL be tried before GET/POST or after?
   * Should calling .all() overwrite all GET/POST/ETC for that url?
   */
  fetch(request) {
    let url = new URL(request.url);

    // Prioritises specificity
    // URL: origin + pathname + search > origin + pathname
    // Method: method > all > default
    if(this.routes[request.method][url.origin + url.pathname + url.search]) {
      return this.routes[request.method][url.origin + url.pathname + url.search](request);
    } else if(this.routes.all[url.origin + url.pathname + url.search]) {
      return this.routes.all[url.origin + url.pathname + url.search](request);
    } else if(this.routes[request.method][url.origin + url.pathname]) {
      return this.routes[request.method][url.origin + url.pathname](request);
    } else if(this.routes.all[url.origin + url.pathname]) {
      return this.routes.all[url.origin + url.pathname](request);
    } else {
      return this.routes.default(request);
    }

  }

  /**
   * Sets the default handler if no others are specified
   */
  default(handler) {
    this.routes.default = handler;
  }

  /**
   * Sets the GET handler for a given URL or Array of URLs
   */
  get(url, handler) {
    this.custom('GET', url, handler);
  }

  /**
   * Sets the POST handler for a given URL or Array of URLs
   */
  post(url, handler) {
    this.custom('POST', url, handler);
  }

  /**
   * Sets the PATCH handler for a given URL or Array of URLs
   */
  patch(url, handler) {
    this.custom('PATCH', url, handler);
  }

  /**
   * Sets the PUT handler for a given URL or Array of URLs
   */
  put(url, handler) {
    this.custom('PUT', url, handler);
  }

  /**
   * Sets the DELETE handler for a given URL or Array of URLs
   */
  delete(url, handler) {
    this.custom('DELETE', url, handler);
  }

  /**
   * Sets the handler for a custom HTTP request to a given URL or Array of URLs
   * @param method is case sensitive
   */
  custom(method, url, handler) {
    if(typeof url === "string") {
      url = [url];
    }
    url.forEach(u => {
      try {
        new URL(u); //relative paths throw an error
      } catch (e) {
        u = self.location.origin + u;
      }

      if(!this.routes[method]) {
        this.routes[method] = {};
      }

      this.routes[method][u] = handler;
    });
  }

  /**
   * Sets the handler for all HTTP requests to a given URL
   * NOTE: This is only tried AFTER attempting to find a request for a specific
   * method
   */
  all(url, handler) {
    this.custom('all', url, handler);
  }

}


// /**
//  * EXAMPLE USAGE
//  */
// var route = new Router();
// var testReq = new Request("https://jsonplaceholder.typicode.com/users");
// var testDefault = new Request("https://jsonplaceholder.typicode.com/posts");
//
// // Defines a custom handler for GET requests to the URL
// route.get('https://jsonplaceholder.typicode.com/users', (request) => {
//
//   var online = Math.floor(Math.random() * 2);
//   if(online) {
//     return fetch(request);
//   } else {
//     return new Promise((resolve, reject) => {
//       resolve(new Response(JSON.stringify({ fake: "true", status: "offline" }), {status: 200, statusText: "OK", headers: {'Content-Type': 'application/json'}}));
//     });
//   }
//
// });
//
// // Fetches the URL which has a specified handler
// route.fetch(testReq).then((response) => {
//   response.json().then(jsonData => {
//     console.log(jsonData);
//   });
// });
//
// // Fetches the URL which doesn't have a specified handler
// route.fetch(testDefault).then((response) => {
//   response.json().then(jsonData => {
//     console.log(jsonData);
//   });
// });
