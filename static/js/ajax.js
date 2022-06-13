function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

$('.like').on('click', function (event) {
	event.preventDefault();
	const url = $(this).attr('data-url');
	const split_url = $(this).attr('data-url').split('/');
	const csrftoken = getCookie('csrftoken');
	const el = $(this)
	const like_css = "far fa-heart"
	const unlike_css = "fas fa-heart"
	$.ajax({
		headers: { 'X-CSRFToken': csrftoken },
		type: 'POST',
		url: url,
		dataType: 'json',
		success: function (response) {
			el.children('span').text(response.likes_count);
			if (response.liked) {
				unlike = el.attr('data-url').replace(split_url[2], 'unlike');
				el.attr('data-url', unlike);
				el.children('i').attr('class', unlike_css)
			} else {
				like = el.attr('data-url').replace(split_url[2], 'like');
				el.attr('data-url', like);
				el.children('i').attr('class', like_css)
			}
		}
	});
});


