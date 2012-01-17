
var PHOTOS_PER_PAGE = 4;
var WORDS_PER_DESC = 16;

function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function trim(str, numWords) {
	var tmp = str.split(" ");
	var ret = str;
	if(tmp.length > numWords)
		ret = tmp.slice(0, numWords).join(" ") + " …";
	return ret;
}


function renderResponse(photos, pageCount, currentPage) {
    if (pageCount == 0) {
        var html = '<p>Brak wyników</p>';
    }
    else {
        var html = '';
        $(photos).each(function(index, photo) {
            html += '<div class="thumbnail">';
            html += '<p><img src="' + photo.thumbnailFile + '"/></p>';
            html += '<div class="desc"><p>' + (photo.description ? escapeHtml(trim(photo.description, WORDS_PER_DESC)) : '<i>brak opisu</i>') + '</p>';
            html += '<p><a href="' + photo.photoPage + '" class="with-icon icon-detail">Szczegóły</a></p></div>';
            html += '</div> ';
        })
        html += '<p>';
        for (var page = 1; page <= pageCount; page++) {
            if (page == currentPage) {
                html += '[Strona ' + page + '] ';
            } else {
                html += '[<a href="javascript: sendRequest(' + page + ')">Strona ' + page + '</a>] ';
            }
        }
        html += '</p>';
    }
    $('#results').html(html)
}

function sendRequest(page) {
    query = $('#search-query').val();
    $.getJSON(
        '/api/search',
        {
            'q': query,
            'o': (page - 1) * PHOTOS_PER_PAGE,
            'l': PHOTOS_PER_PAGE
        },
        function(data) {
            pageCount = Math.ceil(data.totalFound / PHOTOS_PER_PAGE)
            renderResponse(data.photos, pageCount, page)
        }
    );
}

$(function() {
    $('#search-form').submit(function() {
        sendRequest(1)
        return false;
    })
})
