// モーダルで投稿するための関数
function form_submit() {
    const submitButton = document.getElementById("hidden-submit-button");
    submitButton.click();
}

// 講義の評価を計算するための関数
document.addEventListener('DOMContentLoaded', function review_calculator() {
    const star1 = parseInt(document.getElementById("star1").value, 10);
    const star2 = parseInt(document.getElementById("star2").value, 10);
    const star3 = parseInt(document.getElementById("star3").value, 10);
    const star4 = parseInt(document.getElementById("star4").value, 10);
    const star5 = parseInt(document.getElementById("star5").value, 10);
    const result = (star1*1 + star2*2 + star3*3 + star4*4 + star5*5) / ( star1 + star2 + star3 + star4 + star5 );

    // 小数第二位まで求めた結果をuタグに入れる
    const result_round2 = Math.round(result*100) / 100;
    const result_str =  result_round2.toPrecision(3);
    document.getElementById("calculate_result").innerText = result_str;

    // 小数第一位まで求めた結果をdata-rateに入れる
    const result_round1 = Math.round(result*100) / 50;
    const result_floor = Math.floor(result_round1);
    const result_final = (result_floor*5) /10;
    document.querySelector("#star5-rating").dataset.rate = result_final.toPrecision(2);
} );

// 気合でユーザー情報をフォームに入れる
document.addEventListener('DOMContentLoaded', function user_info_input() {
    // ユーザー名を入れる
    document.getElementById("sender_name").value = document.getElementById("sender_name_dummy").value;

    // ユーザーの学類を設定する
    const select_value = document.getElementById("sender_college_dummy").value;
    const select_element = document.getElementById("sender_college");
    const select_options = select_element.options;
    for (let i = 0 ; i < select_options.length ; i++){
        if (select_value === select_options[i].value){
            select_options[i].selected = true;
            break;
       }
    }
} );
 