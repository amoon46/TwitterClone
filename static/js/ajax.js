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
	const csrftoken = getCookie('csrftoken');
	const selector = $(this)
	$.ajax({
		headers: { 'X-CSRFToken': csrftoken },
		type: 'POST',
		url: url,
		dataType: 'json',
		success: function (response) {
			selector.children('span').text(response.likes_count);
			if (response.liked) {
				selector.attr('data-url', '/unlike/num/'.replace(/num/, response.post_pk));
				selector.children('i').attr('class', 'fas fa-thumbs-up')
			} else {
				selector.attr('data-url', '/like/num/'.replace(/num/, response.post_pk));
				selector.children('i').attr('class', 'far fa-thumbs-up')
			}
		}
	});
});


