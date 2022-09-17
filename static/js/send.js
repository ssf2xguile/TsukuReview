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
        }
    },
}).mount('#send_app');