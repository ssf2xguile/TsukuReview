Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            // MAXLENGTH_TITLE: document.getElementById('titleFormControlTextarea1').maxlength,
            // MAXLENGTH_OVERALL: document.getElementById('overallFormControlTextarea1').maxLength,
            // MAXLENGTH_DIFFICULTY: document.getElementById('difficultyFormControlTextarea1').maxLength,
            // MAXLENGTH_KADAI: document.getElementById('kadaiFormControlTextarea1').maxLength,
            // MAXLENGTH_EVALUATION: document.getElementById('evaluationFormControlTextarea1').maxLength,
            inputTitle: "",
            inputOverall: "",
            inputDifficulty: "",
            inputKadai: "",
            inputEvaluation: "",
            submitbutton: "",
        }
    },
}).mount('#send_app');


// vue.jsで以下の関数を実装する方法を思いつかなかったから、通常のjavascriptで記述する
function form_submit() {
    const submitButton = document.getElementById("hidden-submit-button");
    submitButton.click();
}

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