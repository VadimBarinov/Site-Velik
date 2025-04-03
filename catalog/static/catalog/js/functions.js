function clickOnStar(id_star){

    for (let i = 1; i <= id_star; i++){
        $('#star-modal-' + i).attr('src', grad_star);
    }
    for (let i = id_star+1; i <= 5; i++){
        $('#star-modal-' + i).attr('src', black_star);
    }

    $('[name=count_stars]').attr('value', id_star)

}

function currentStarsBike(id_star, id_bike){

    for (let i = 1; i <= id_star; i++){
        $('#star-' + i + '-' + id_bike).attr('src', grad_star);
    }
    for (let i = id_star+1; i <= 5; i++){
        $('#star-' + i + '-' + id_bike).attr('src', black_star);
    }

}