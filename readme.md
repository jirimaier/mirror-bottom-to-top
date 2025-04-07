# Mirror Bottom to Top KiCAD Plugin

This KiCad action plugin mirrors all bottom copper tracks and filled shapes (circles, rectangles, polygons, etc.) to the top copper layer across horizontal axis passing through drill/place origin.

It adds a button to tollbar. If something exists in top layer, clicking the button will delete it. If top layer is empty, clicking the button will crete the mirrored version on bottom in top. (So refreshing the top layer after bottom is changed requires two clicks)

## Instalation
Download the mirror-bottom-to-top.zip from Releases.
In KiCAD, open **Plugin and Content Manager** and click **Install from File**. 
Select the zip file you downloaded.

