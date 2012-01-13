
var PHOTOS_PER_PAGE = 20;

function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
            html += '<p>' + (photo.description ? escapeHtml(photo.description) : '<i>brak opisu</i>') + '</p>';
            html += '<p><a href="' + photo.photoPage + '" class="with-icon icon-detail">Szczegóły</a></p>';
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
