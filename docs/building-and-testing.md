---
title: 4. Building and Testing
showsocial: False
...

To build your site run

~~~ .bash  
$ make
~~~

All files are written to the `www/` folder (or whatever you have indicated in your `config.ini`.

To test your site run

~~~ .bash 

$ make serve
~~~

(press `^C` to exit the server).  If you are confident that the build will succeed, you may use

~~~ .bash 
$ make && make serve
~~~

instead.



*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Writing Content](writing-content.html) |
[Top](index.html) |
[Styling Content >>](styling-content.html)
</nav>
