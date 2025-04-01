$(document).ready(function () {
    $('form[name=formDeleteStar]').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            url: currentUrl,
            type: "POST",
            dataType: "json",
            success: function (response) {
                $('#AddStarModal').modal('hide');
                if (response.is_taken == true) {
                    clickOnStar(0);
                    $('#myStar').addClass('text-grey');
                    $('#myStar').text('оценить');
                    $('#myStarValue').text('');
                    if (response.star_bike == 0) {
                        $('#bikeStarImg').attr('src', black_star);
                        $('#bikeStar').addClass('text-grey');
                        $('#bikeStar').text('нет оценок');
                    }
                    else {
                        $('#bikeStarImg').attr('src', grad_star);
                        $('#bikeStar').removeClass('text-grey');
                        $('#bikeStar').text(parseFloat(response.star_bike).toFixed(1).replace(".",","));
                    }
                }
            }
        });
        return false;
    });
})