function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

async function deleteKeyword(keyword_id) {
	try {
		res = await fetch("http://127.0.0.1:8000/auth/delete_word/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			body: JSON.stringify({
				keyword_id: keyword_id,
			}),
		});
		console.log(await res.json());
	} catch (e) {
		console.log(e);
	}
}