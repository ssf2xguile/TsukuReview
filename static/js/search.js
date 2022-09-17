Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            results: {},                        //検索結果
            query: "",                          //検索キーワード
            latest_request_time : Date.now()    //最新の検索実行要求時刻
        };
    },
    methods: {
        inputEvent(event) {
            //検索ボックスの内容が変更されるたびに呼ばれる
            const input_value = event.target.value.trim();
            this.searchAndDataUpdate(input_value);
        },
        async searchAndDataUpdate(input_value) {
            if (!input_value) {
                this.results = {};
                this.query = "";
            }else{    
                //APIリクエストは非同期のため、重いリクエストの後に軽いリクエストを送ると
                //軽い＝＞重いの順に到着してしまい、結果がおかしくなります。
                //そのため、時刻を使って最新のリクエストのみデータを更新するようにしています。
                const called_time = Date.now();
                this.latest_request_time = called_time;

                const ret = await axios.get(
                    `/api/search_subjects?q=${input_value}`
                );
                
                if (this.latest_request_time == called_time) {
                    this.results = ret.data;
                    this.results = this.review_count(this.results);
                    this.query = input_value;
                }                
            }
        },
        readmoreFilter(text, max_length, suffix) {
            //長いテキストを省略表記にする
            //readmoreFilter("ABC", 4, "...") => "ABC"
            //readmoreFilter("ABCD", 2, "...") => "AB..."
            if (text.length < max_length) return text;
            return text.substring(0, max_length) + suffix;
        },
        review_count (result) {
            for (let sub in result){
                sub.review_count = sub.star1+sub.star2+sub.star3+sub.star4+sub.star5;
            }
            return result;   
        },
        review_calculator(event) {
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
        }
    }
}).mount('#search_app')
