// モーダルで投稿するための関数
function form_submit() {
    const submitButton = document.getElementById("hidden-submit-button");
    submitButton.click();
}

document.addEventListener('DOMContentLoaded', function review_calculator() {
    const star1 = parseInt(document.getElementById("star1").value, 10);
    const star2 = parseInt(document.getElementById("star2").value, 10);
    const star3 = parseInt(document.getElementById("star3").value, 10);
    const star4 = parseInt(document.getElementById("star4").value, 10);
    const star5 = parseInt(document.getElementById("star5").value, 10);
    
    const result = (star1*1 + star2*2 + star3*3 + star4*4 + star5*5) / ( star1 + star2 + star3 + star4 + star5 );

    const result_str =  String(Math.round(result, 0.5));
    console.log(result_str);
    document.getElementById("calculate_result").innerText = result_str;
    document.querySelector("#star5-rating").dataset.rate = result_str;
} );
 