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

        var subPk = $(this).val();
        var selectedPk = $('h4').get(0).id;

        $.ajax({
            url: "/foods/save/",
            method: "POST",
            data: {
                selected: selectedPk,
                sub: subPk
            },
            success: (data, textStatus, xhr) => {
                // if ($(".alert").length) {
                //     $(".alert").hide();
                // }
                $(this).hide();
                $(this).parent().html('<i class = "check fas fa-check-circle" ></i>');
            },
            error: () => {
                var error = "Une erreur interne est apparue. Merci de recommencer votre requête."
                $("section>div.container").prepend("<div class=\"alert alert-warning\">" + error + "</div>")

            }


        });
    });



    $(".product-title").each(function () {
        $(this).html($(this).html().replace(new RegExp("None", "g"), ""));
    });




});