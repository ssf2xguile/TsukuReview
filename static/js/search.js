Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            results: {},                        //検索結果
            query: "",                          //検索キーワード
            hitcount: 0,                        //検索ヒット数
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
                this.hitcount = 0;
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
                    this.hitcount = Object.keys(this.results).length;
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
        getSchoolsClass(school) {
            //学群から背景色を指定するクラスを得る
            const schools_class_dict = {
                'グローバル教育院 地球規模課題学位プログラム': 'college-img-small color-navy',
                'フレッシュマン・セミナー': 'college-img-small color-beige',
                '医学群':                   'college-img-small color-pink',
                '外国語':                   'college-img-small color-pastel-green',
                '学士基盤科目':             'college-img-small color-teal',
                '学士基盤科目（高年次向け）': 'college-img-small color-teal',
                '学問への誘い':             'college-img-small color-teal',
                '教職に関する科目':          'college-img-small color-vintage-orange',
                '芸術':                     'college-img-small color-light-green',
                '芸術専門学群':             'college-img-small color-brown',
                '国語':                     'college-img-small color-pale-pink',
                '自由科目（特設）':         'college-img-small color-pale-gray',
                '社会・国際学群':           'college-img-small color-orange',
                '情報':                     'college-img-small color-pale-purple',
                '情報学群':                 'college-img-small color-purple',
                '人間学群':                 'college-img-small color-yellow',
                '人文・文化学群':           'college-img-small color-pale-red',
                '生命環境学群':             'college-img-small color-light-green',
                '全学群対象':               'college-img-small color-color-beige',
                '体育':                     'college-img-small color-pale-teal',
                '体育専門学群':             'college-img-small color-white-blue',
                '日本事情等科目':           'college-img-small color-pale-gray',
                '博物館に関する科目':       'college-img-small color-pale-gray',
                '理工学群':                 'college-img-small color-dark-blue',
                '':                        'college-img-small color-pale-gray',
            };
            return schools_class_dict[school];
        },
        SimplifySchoolsName(school) {
            //学群から背景色を指定するクラスを得る
            const schools_class_dict = {
                'グローバル教育院 地球規模課題学位プログラム': 'グローバル',
                'フレッシュマン・セミナー': 'フレセミ',
                '医学群':                   '医',
                '外国語':                   '外国語',
                '学士基盤科目':             '学士基盤',
                '学士基盤科目（高年次向け）': '学士基盤',
                '学問への誘い':             '学問',
                '教職に関する科目':          '教職',
                '芸術':                     '芸術',
                '芸術専門学群':             '芸専',
                '国語':                     '国語',
                '自由科目（特設）':         '自由科目',
                '社会・国際学群':           '社会',
                '情報':                     '情報',
                '情報学群':                 '情報',
                '人間学群':                 '人間',
                '人文・文化学群':           '人文',
                '生命環境学群':             '生命',
                '全学群対象':               '全学群',
                '体育':                     '体育',
                '体育専門学群':             '体専',
                '日本事情等科目':           '日本事情',
                '博物館に関する科目':       '博物館',
                '理工学群':                 '理工',
                '':                        'データなし',
            };
            return schools_class_dict[school];
        },
        ValidateData(value) {
            //データのチェック
            if (value === '') {
                return 'データなし';
            } else {
                return value;
            }
        },
    }
}).mount('#search_app')
