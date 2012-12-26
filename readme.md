#Compressing GeoJSON

GeoJSON can get quite big when you need represent complex maps with lots of polygons. Even though it compresses well, being text, 
it can still be quite a hassle to store and upload to a website in uncompressed form. 

Recently while working on a web app which requires the upload of maps in GeoJSON format, I stumbled upon Google App Engine's 
limitation of 32MB for POST requests. At that point I realized that I'd have to look for a way to compress it before uploading,
but rather that just asking users to gzipping before uploading, I decided to look into ways to make a GeoJSON map lighter by 
eliminating redundancies and perhaps reducing the level of detail a little bit. You see, a single polygon (representing a state 
or a county), may be composed of thousands of points, each one represented by an array of two floating point numbers. That's 
**a lot** of bytes!

Soon my search took me to TopoJSON by Mike Bostok, which is great but is not compatible with GeoJSON, so it was not what I was 
looking for. But reading about TopoJSON, led me to LilJSON and this paper: www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html

After looking at those resources, it was time to get my fingers typing. So I forked LilJSON which already achieved some compression by
reducing the precision of the floating points in the GeoJSON. After a while I had a mildly improved version of it, which contributed 
back via Pull Request. I then set out to implement Visvalingam's algorithm, which aimed a simplifying polygonal lines while trying 
not to alter too much the original area (and shape) of the polygon.

I was very surprised to find out that both techniques combined, the reduction of coordinate precision and the simplification
of lines, yielded a very nice compression of my test GeoJSON: It went from 62MB to a mere 5.1MB!! And all of this could still be reduced by
a factor of ten by Gzipping it.

Just to check how well my compressed version stood up to the original, I opened both in Quantum GIS and was blown away, the 
differences were tiny! only maginifying A LOT, I was able to see the the diferences. I am not including an image here to 
encourage you to try for yourself. ;-)