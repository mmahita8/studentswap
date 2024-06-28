// simulated search feature that shows results for keywords=electronics/devices/computers. if keyword doesn't match,
// it'll show a user-friendly error message

$(document).ready(function() {

        var query = window.location.search;

        var urlparams = new URLSearchParams(query);
        var keyword = urlparams.get("searchitems");

        if (keyword.toLowerCase() === "electronics" || keyword.toLowerCase() ==="computers" || keyword.toLowerCase()==="devices") {

         var itemresults=$(

             "  <div class=\"itemscontainer\">\n" +
             "     <div class=\"item\">\n" +
             "\n" +
             "        <div class=\"imgclass\">\n" +
             "            <img src=\"static\\images\\electronic-devices\\alexandru-acea-rmHTCPXUk9g-unsplash.jpg\" alt=\"LG UltraWide QHD 34-Inch Curved Computer Monitor\">\n" +
             "        </div>\n" +
             "        <div class=\"info\">\n" +
             "         <div class=\"iteminfo\">\n" +
             "            <div class=\"rating\">\n" +
             "                <p class=\"itemtext\">LG UltraWide QHD 34-Inch Curved Computer Monitor</p>\n" +
             "                <i class=\"fa-regular fa-heart itemtext\"></i>\n" +
             "            </div>\n" +
             "\n" +
             "            <p class=\"itemtext\">$246.39</p>\n" +
             "            <a href=\"\" class=\"itemtext\">More info</a>\n" +
             "         </div>\n" +
             "        </div>\n" +
             "    </div>\n" +
             "    <div class=\"item\">\n" +
             "        <div class=\"imgclass\">\n" +
             "            <img src=\"studentswap\\static\\images\\electronic-devices\\howard-bouchevereau-S2r2Ex8jv2o-unsplash.jpg\" alt=\"Apple Macbook Air 13-inch\">\n" +
             "        </div>\n" +
             "        <div class=\"info\">\n" +
             "         <div class=\"iteminfo\">\n" +
             "            <div class=\"rating\">\n" +
             "                <p class=\"itemtext\">Apple Macbook Air 13-inch</p>\n" +
             "                <i class=\"fa-regular fa-heart\"></i>\n" +
             "            </div>\n" +
             "\n" +
             "            <p class=\"itemtext\">$700.00</p>\n" +
             "            <a href=\"\" class=\"itemtext\">More info</a>\n" +
             "         </div>\n" +
             "        </div>\n" +
             "    </div>\n" +
             "\n" +
             "    </div>"
            );


           $(".searchresults").append(itemresults);
        }
        else {
            // window.alert("xx");
            displayerror();

        }

 function displayerror()
{
    var noresult=$("<br><div id='noresultmsg'>No items matched your search, try again!</div><br>");
    $('.viewed').siblings('.results').append(noresult).css({"font-size": "1.7rem", "color": "red"});
}



});
