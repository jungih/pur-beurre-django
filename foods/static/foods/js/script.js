$(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
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

    $("button.save").on("click", function () {
        var code = $(this).val();
        var sub = document.getElementById(code).textContent;
        var product = document.getElementById("selected").textContent;

        $.ajax({
            url: "/foods/save/",
            method: "POST",
            data: {
                product: product,
                sub: sub
            },
            success: () => {
                $(this).hide();
            }

        })
    });


    $(".name").each(function () {
        $(this).text($(this).text().replace(new RegExp(" - None", "g"), ""));
    });




});