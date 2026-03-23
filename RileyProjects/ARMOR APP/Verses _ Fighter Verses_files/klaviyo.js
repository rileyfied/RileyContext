(function(){
    var kv_app_id = "56ef2e6d-735c-47ec-a639-fb67bb9c892e";
    var kv_ajax_url = "https://wix.presto-changeo.com/klaviyo/front/";

    var poco_kl_settings = poco_kl_settings || null;
    var poco_kl = poco_kl || null;
    var pocoApiKey = pocoApiKey || null;
    var poco_plan = poco_plan || null;
    var id_popup = id_popup || null;
    var pages_number = pages_number || null;
    var company_id = company_id || null;
    var display_popup = display_popup || null;
    var popup_delay = popup_delay || null;
    var signups = signups || null;
    var popupFrequency = popupFrequency || null;

    // var _learnq = _learnq || [];

    // window.addEventListener("load", function () {
        poco_kl_settings = document.getElementById("poco-kl-settings");

        if (poco_kl_settings) {
            if (poco_kl_settings.hasAttribute('src')) {
                fetch(poco_kl_settings.src)
                  .then(response => response.text())
                  .then(function(data){
                        poco_kl = JSON.parse(atob(html_entity_decode(data).trim().replaceAll('&#x3D;', '=').replaceAll("\&#x2F;", '/').replaceAll('\\', '').replaceAll('"', '')));
                        pocoApiKey = poco_kl.key;
                        poco_plan = poco_kl.plan;
                        display_popup = parseInt(poco_kl.display_popup);
                        popup_delay = poco_kl.popup_delay;
                        id_popup = poco_kl.id_popup;
                        pages_number = poco_kl.pages_count;
                        company_id = poco_kl.company_id;
                        signups = poco_kl.signups || 0;
                        isOrdersSyncActive = poco_kl.isOrdersSyncActive || false;
                        popupFrequency = poco_kl.popup_frequency || 0;
                  });
            } else {
                poco_kl = cleanJsonStr(poco_kl_settings.innerHTML);
                pocoApiKey = poco_kl.key;
                poco_plan = poco_kl.plan;
                display_popup = parseInt(poco_kl.display_popup);
                popup_delay = poco_kl.popup_delay;
                id_popup = poco_kl.id_popup;
                pages_number = poco_kl.pages_count;
                company_id = poco_kl.company_id;
                signups = poco_kl.signups || 0;
                isOrdersSyncActive = poco_kl.isOrdersSyncActive || false;
                popupFrequency = poco_kl.popup_frequency || 0;
            }

            console.log('poco_kl = ', poco_kl);
        } else {
            var urlParam = poco_getURLParam(document.getElementById("poco-kl-script").src, "pocoApiKey");
            var keys = urlParam.split("::");
            (typeof keys[0] !== "undefined") && (pocoApiKey = keys[0]);
            (typeof keys[1] !== "undefined") && (pages_number = keys[1]);
            (typeof keys[2] !== "undefined") && (company_id = keys[2]);

            poco_plan = 'advanced';
            isOrdersSyncActive = true;
        }

        let wix_events_interval_1 = setInterval(function () {
          if (poco_kl || !poco_kl_settings) {
            clearInterval(wix_events_interval_1);
            initKVTrackingScript();
            kvTrackMember();
          }
        }, 20);

        document.addEventListener("click", function (e) {
            if (
                e.target.closest("[data-testid='buttonElement']") ||
                (e.target.hasAttribute("data-testid") && e.target.getAttribute("data-testid") === "buttonElement")
            ) {
                _learnq.push(['identify', {
                    '$email': e.target.closest("form").querySelector('[type="email"]').value
                }]);
            }
        });
    // });

    if (typeof window.wixDevelopersAnalytics !== 'undefined') {
        let wix_events_interval = setInterval(function () {
          if (poco_kl || !poco_kl_settings) {
            clearInterval(wix_events_interval);
            initKV();
          }
        }, 20);
    } else {
        window.addEventListener('wixDevelopersAnalyticsReady', function () {
          let wix_events_interval = setInterval(function () {
            if (poco_kl || !poco_kl_settings) {
              clearInterval(wix_events_interval);
              initKV();
            }
          }, 20);
        });
    }

    function kikosPopup (selector, options) {
        options = options || {};
        this.settings = Object.assign({}, this.defaults, options);
        this.is_opened = false;
        this.overlay = null;
        this.popup = document.querySelector(selector);
        this.init();

        return this;
    }
    kikosPopup.prototype = {
        "defaults" : {
            "width" : 300,
            "height" : 300,
            "autoshow" : false,
            "overlay_enable" : true,
            "overlay_bgColor" : "#fff",
            "overlay_opacity" : 0.5
        },
        init : function () {
            if ( this.settings.overlay_enable ) {
                this._initOverlay();
            }

            this._initPopup();
            this._initEvents();

            if ( this.settings.autoshow ) {
                this.open();
            }
        },
        _initOverlay : function () {
            this.overlay = document.createElement("div");
            this.overlay.classList.add("kikosPopup-overlay");
            this.overlay.style.display = "none";

            document.body.append(this.overlay);

            this.overlay.style.position = "fixed";
            this.overlay.style.top = 0;
            this.overlay.style.left = 0;
            this.overlay.style.right = 0;
            this.overlay.style.bottom = 0;
            this.overlay.style.backgroundColor = this.settings.overlay_bgColor;
            this.overlay.style.opacity = this.settings.overlay_opacity;
            this.overlay.style.zIndex = 99998;
        },
        _initPopup : function () {
            if (!this.settings.width) {
                this.settings.width = document.querySelector('.poco-popup-wrapper').clientWidth;
            }

            if (window.innerWidth <= this.settings.width) {
                var left = 0;
                var margin_left = 0;
            } else {
                var left = "50%";
                var margin_left = "-" + (this.settings.width / 2) + "px";
            }

            this.popup.style.display = "none";

            // document.body.append(this.popup);

            this.popup.style.background = "transparent";
            this.popup.style.position = "fixed";
            this.popup.style.top = 0;
            this.popup.style.left = left;
            this.popup.style.bottom = 0;
            this.popup.style.width = this.settings.width + "px";
            this.popup.style.marginTop = "auto";
            this.popup.style.marginLeft = margin_left;
            this.popup.style.marginBottom = "auto";
            this.popup.style.zIndex = 99999;
        },
        _initEvents : function () {
            var self = this;
            this.overlay.addEventListener("click", function () {
                self.close();
            });
        },
        open : function () {
            var self = this;

            this.fadeIn(this.overlay, null, 0.6);
            setTimeout(function(){
                self.fadeIn(self.popup, function (popup_obj) {
                    self.is_opened = true;
                });
            }, 500);
        },
        close : function () {
            var self = this;

            this.fadeOut(this.overlay);
            this.fadeOut(this.popup, function (popup_obj) {
                popup_obj.is_opened = false;
            });
        },
        fadeIn : function (el, callback, opacity) {
            var self = this;

            opacity = opacity || 1;
            callback = callback || function () {};

            el.style.opacity = 0;
            el.style.display = "flex";

            (function fade() {
                var val = parseFloat(el.style.opacity);
                if (!((val += 0.1) > opacity)) {
                    el.style.opacity = val;
                    requestAnimationFrame(fade);
                } else {
                    callback(self);
                }
            })();
        },
        fadeOut : function (el, callback, opacity) {
            var self = this;

            opacity = opacity || 0;
            callback = callback || function () {};

            el.style.opacity = 1;

            (function fade() {
                if ((el.style.opacity -= 0.1) < opacity) {
                    el.style.display = "none";
                    callback(self);
                } else {
                    requestAnimationFrame(fade);
                }
            })();
        }   
    };

    function dobPicker (params) {
        // apply defaults
        (typeof(params.dayDefault) == "undefined") && (params.dayDefault = "Day");
        (typeof(params.monthDefault) == "undefined") && (params.monthDefault = "Month");
        (typeof(params.yearDefault) == "undefined") && (params.yearDefault = "Year");
        (typeof(params.minimumAge) == "undefined") && (params.minimumAge = 18);
        (typeof(params.maximumAge) == "undefined") && (params.maximumAge = 100);

        // find elements
        var dayElement = document.querySelector(params.daySelector);
        var monthElement = document.querySelector(params.monthSelector);
        var yearElement = document.querySelector(params.yearSelector);

        // set days
        if (dayElement) {
            let opt = document.createElement("option");
            opt.innerText = params.dayDefault;
            opt.value = "0";
            dayElement.append(opt);
            for (var i = 1; i <= 31; i++) {
                let val = ("" + i).padStart(2, 0);
                let opt = document.createElement("option");
                opt.value = val;
                opt.innerText = val;
                dayElement.append(opt);
            }
        }

        // set months
        if (monthElement) {
            var months = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ];

            let opt = document.createElement("option");
            opt.innerText = params.monthDefault;
            opt.value = "0";
            monthElement.append(opt);
            for (var i = 1; i <= 12; i++) {
                let val = ("" + i).padStart(2, 0);
                let opt = document.createElement("option");
                opt.value = val;
                opt.innerText = months[i - 1];
                monthElement.append(opt);
            }
        }

        // set years
        if (yearElement) {
            var now = (new Date()).getFullYear();
            var minimum = now - params.minimumAge;
            var maximum = minimum - params.maximumAge;

            let opt = document.createElement("option");
            opt.innerText = params.yearDefault;
            opt.value = "0";
            yearElement.append(opt);

            for (i = minimum; i >= maximum; i--) {
                var year = "" + i;
                let opt = document.createElement("option");
                opt.value = year;
                opt.innerText = year;
                yearElement.append(opt);
            }
        }

        // disable months
        if (dayElement) {
            dayElement.addEventListener("change", function () {
                if (yearElement) {
                    yearElement.querySelectorAll("option").forEach(function (el) {
                        el.removeAttribute("disabled");
                    });
                }

                var day = parseInt(dayElement.value);

                if (day >= 1 && day <= 29) {
                    monthElement.querySelectorAll("option").forEach(function (el) {
                        el.removeAttribute("disabled");
                    });
                } else if (day == 30) {
                    monthElement.querySelectorAll("option").forEach(function (el) {
                        el.removeAttribute("disabled");
                    });
                    monthElement.querySelector('option[value="02"]').setAttribute("disabled", "disabled");
                } else if (day == 31) {
                    monthElement.querySelectorAll("option").forEach(function (el) {
                        el.removeAttribute("disabled");
                    });
                    monthElement.querySelector('option[value="02"]').setAttribute("disabled", "disabled");
                    monthElement.querySelector('option[value="04"]').setAttribute("disabled", "disabled");
                    monthElement.querySelector('option[value="06"]').setAttribute("disabled", "disabled");
                    monthElement.querySelector('option[value="09"]').setAttribute("disabled", "disabled");
                    monthElement.querySelector('option[value="11"]').setAttribute("disabled", "disabled");
                }
            });
        }
    }

    function poco_getURLParam (url, key) {
        var p = {};
        url.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(s, k, v){p[key] = v});
        return key ? p[key] : p;
    }

    function requestAndDisplayPopup (pocoApiKey) {
        if (popupFrequency == 1) {
            if (sessionStorage.getItem('poco_popup') == 1 || localStorage.getItem('poco_popup_subscribed') == 1) {
                return false;
            }
        } else {
            if (localStorage.getItem("poco_popup") == 1) {
                return false;
            }
        }

        if (signups >= 100 && poco_plan == 0) {
            return false;
        }

        if (poco_kl) {
            console.log('KV display_popup 2', display_popup);
            if (!display_popup || !validateTargeting(poco_kl.popup_settings)) {
                return false;
            }

            setTimeout(function() {
                renderPopup();
            }, poco_kl.popup_delay * 1000);
        } else {
            poco_ajax(
                kv_ajax_url,
                "GET",
                {
                    "action": "getPopup",
                    "apiKey": pocoApiKey
                },
                function (data) {
                    if (
                        localStorage.getItem("poco_popup") == 1 ||
                        !data.displayPopup ||
                        !validateTargeting(data.popup_settings)
                    ) {
                        return false;
                    }

                    (function(data){ 
                        setTimeout(function() {
                            displayKLPopup(data)
                        }, data.popupDelay * 1000);
                    })(data);
                }
            );
        }
    }

    function validateTargeting(popup_settings) {
        let show = true;

        if (popup_settings.display_on_page == 2) {
            if (location.pathname !== "/") {
                show = false;
            }
        } else if (popup_settings.display_on_page == 3) {
            let url_or_keywords = popup_settings.display_on_page_url_keyword.split(",");

            let j = 0;
            url_or_keywords.forEach(function (keyword) {
                if (
                    (keyword.trim().indexOf("http") !== -1 && location.href.replace(location.search, "") !== keyword.trim()) ||
                    (keyword.trim().indexOf("http") === -1 && location.href.indexOf(keyword.trim()) === -1)
                ) {
                    j++;
                }
            });
            if (j == url_or_keywords.length) {
                show = false;
            }
        }

        if (show) {
            if (popup_settings.exclude_page == 2) {
                if (location.pathname == "/") {
                    show = false;
                }
            } else if (popup_settings.exclude_page == 3) {
                let keywords = popup_settings.exclude_page_url_keyword.split(",");
                keywords.forEach(function (keyword) {
                    if (
                        (keyword.trim().indexOf("http") !== -1 && location.href.replace(location.search, "") === keyword.trim()) ||
                        (keyword.trim().indexOf("http") === -1 && location.href.indexOf(keyword.trim()) !== -1)
                    ) {
                        show = false;
                    }
                });
            }
        }

        return show;
    }

    function displayKLPopup (data) {
        if (document.querySelectorAll(".kikosPopup-poco-klaviyo").length > 0) {
            return false;
        }

        var kikosPopup_poco = document.createElement("div");
        kikosPopup_poco.classList.add("kikosPopup-poco-klaviyo");
        kikosPopup_poco.style.display = "none";
        document.body.append(kikosPopup_poco);
        kikosPopup_poco.innerHTML = data.content;

        setupKikosPopup("kikosPopup-poco-klaviyo", data);
    }

    function renderPopup () {
        console.log('KV display_popup = ', display_popup);
        if (!display_popup) {
            return false;
        }

        if (document.querySelectorAll(".kikosPopup-poco-klaviyo").length > 0) {
            return false;
        }

        let ps = poco_kl.popup_settings;
        if (id_popup >= 0 && id_popup <= 3) {
            let template_css = createDOMElement("link", {"rel" : "stylesheet", "href" : kv_ajax_url + '/assets/css/templates/template-'+id_popup+'.css'}, null, document.body);
            if (typeof ps.font !== "undefined") {
                let font_name = ps.font.split(",")[0].trim().replaceAll("&#39;", "").replace(/["']/g, "");
                let font = createDOMElement("link", {"rel" : "stylesheet", "href" : "https://fonts.googleapis.com/css2?family=" + font_name + "&display=swap"}, null, document.body);

                let font_css = ".poco-popup-wrapper * {font-family: " + ps.font + "}";
                let head = document.head || document.getElementsByTagName('head')[0];
                let style = document.createElement('style');

                head.appendChild(style);
                style.type = 'text/css';
                style.appendChild(document.createTextNode(font_css));
            }
            template_css.addEventListener("load", function () {
                createDOMElement(
                    "div", {"class" : "kikosPopup-poco-klaviyo"}, null, document.body,
                    createDOMElement(
                        "section", {"class" : "poco-popup-wrapper", "data-template" : id_popup},
                        {
                            "backgroundColor" : (id_popup == 3 ? ps.bg_color : null),
                            "fontFamily" : (ps.font ? ps.font : "")
                        }, null,
                        createDOMElement(
                            "div", {"class" : "poco-popup-content"},
                            {
                                "backgroundColor" : (id_popup != 3 ? ps.bg_color : null),
                                "backgroundImage" : (id_popup != 3 ? "url('" + ps.background + "')" : null)
                            }, null,
                            function () {
                                let r = [];

                                if (ps.background) {
                                    if ((id_popup == 0 || id_popup == 1 || id_popup == 2)) {
                                        r.push(createDOMElement(
                                            "img",
                                            {
                                                "id" : "popup_bg_image",
                                                "src" : ps.background,
                                                "style" : "display:none !important;"
                                            }
                                        ));
                                    }

                                    if (id_popup == 3) {
                                        r.push(
                                            createDOMElement(
                                                "div", {"class" : "popco-popup-section-2"}, null, null,
                                                createDOMElement("img", {"src" : ps.background})
                                            )
                                        );
                                    }
                                }

                                if (id_popup == 3) {
                                    r.push(
                                        createDOMElement("div", {"class" : "popco-popup-section-1"}, null, null, function () {
                                            let texts = [];
                                            if (ps.text_line_1) {
                                                texts.push(createDOMElement("h2", null, null, null, ps.text_line_1));
                                            }
                                            if (ps.text_line_2) {
                                                texts.push(createDOMElement("h3", null, null, null, nl2br(ps.text_line_2)));
                                            }
                                            return texts;
                                        })
                                    )
                                } else {
                                    ps.text_line_1 && r.push(createDOMElement("h2", null, null, null, ps.text_line_1));
                                    ps.text_line_2 && r.push(createDOMElement("h3", null, null, null, nl2br(ps.text_line_2)));
                                }


                                r.push(
                                    createDOMElement("ul", {"class" : "poco-popup-inputs"}, null, null,
                                        function () {
                                            let li = [];

                                            if (ps.display_name_field) {
                                                li.push(createDOMElement(
                                                    "li", {"class" : "poco-popup-name-block poco-clearfix"}, null, null,
                                                    [
                                                        createDOMElement(
                                                            "div", {"class" : "poco-popup-first-name"}, null, null,
                                                            createDOMElement(
                                                                "input",
                                                                {
                                                                    "type" : "text",
                                                                    "name" : "popuppoco_newsletter_name",
                                                                    "id" : "popuppoco_newsletter_name",
                                                                    "placeholder" : ps.name_placeholder
                                                                }
                                                            ),
                                                        ),
                                                        createDOMElement(
                                                            "div", {"class" : "poco-popup-last-name"}, null, null,
                                                            createDOMElement(
                                                                "input",
                                                                {
                                                                    "type" : "text",
                                                                    "name" : "popuppoco_newsletter_lname",
                                                                    "id" : "popuppoco_newsletter_lname",
                                                                    "placeholder" : ps.lname_placeholder
                                                                }
                                                            )
                                                        )
                                                    ]
                                                ));
                                            }

                                            if (id_popup != 3) {
                                                li.push(createDOMElement(
                                                    "li",
                                                    null, null, null,
                                                    createDOMElement(
                                                        "input",
                                                        {
                                                            "type" : "email",
                                                            "name" : "popuppoco_newsletter_email",
                                                            "id" : "popuppoco_newsletter_email",
                                                            "placeholder" : ps.email_placeholder
                                                        }
                                                    )
                                                ));
                                            }

                                            if (ps.display_dob_field) {
                                                li.push(createDOMElement(
                                                    "li",
                                                    null, null, null,
                                                    [
                                                        createDOMElement("div", {"class" : "dob-label"}, null, null, ps.dob_label),
                                                        createDOMElement(
                                                            "div", {"class" : "dob-items"}, null, null,
                                                            [
                                                                createDOMElement("select", {"id" : "dobday"}),
                                                                createDOMElement("select", {"id" : "dobmonth"})
                                                            ]
                                                        )
                                                    ]
                                                ));
                                            }

                                            li.push(createDOMElement(
                                                "li",
                                                {"class" : (id_popup == 3 ? "poco-popup-form-group" : null)},
                                                null, null,
                                                [
                                                    (id_popup == 3 ? createDOMElement(
                                                        "li",
                                                        null, null, null,
                                                        createDOMElement(
                                                            "input",
                                                            {
                                                                "type" : "email",
                                                                "name" : "popuppoco_newsletter_email",
                                                                "id" : "popuppoco_newsletter_email",
                                                                "placeholder" : ps.email_placeholder
                                                            }
                                                        )
                                                    ) : null),
                                                    createDOMElement(
                                                        "button",
                                                        {
                                                            "type" : "submit",
                                                            "class" : "poco-popup-newsletter-submit",
                                                            "id" : "poco-popup-newsletter-submit",
                                                        },
                                                        null, null, ps.submit_button_text
                                                    ),
                                                    (
                                                        ps.close_button_text && id_popup == 3 ?
                                                            createDOMElement(
                                                                "button",
                                                                {
                                                                    "type" : "submit",
                                                                    "class" : "poco-popup-close-icon kikos-close-btn"
                                                                },
                                                                null, null, ps.close_button_text
                                                            ) : null
                                                    )
                                                ]
                                            ));

                                            li.push(createDOMElement(
                                                "li", null, null, null,
                                                (
                                                    ps.close_button_text && id_popup == 1 ?
                                                        createDOMElement(
                                                            "button",
                                                            {
                                                                "type" : "submit",
                                                                "class" : "poco-popup-close-button kikos-close-btn",
                                                                "style" : "background-color: " + ps.close_button_bg_color
                                                            },
                                                            null, null, ps.close_button_text
                                                        ) : null
                                                )
                                            ));

                                            return li;
                                        }
                                    )
                                );

                                r.push(
                                    createDOMElement(
                                        "button", {"class" : "poco-popup-close-icon kikos-close-btn"}, null, null, "X"
                                    )
                                );

                                return r;
                            }
                        )
                    )
                );
                
                setupKikosPopup("kikosPopup-poco-klaviyo", ps);
            });
        } else if (id_popup == 1000) {
            createDOMElement("div", {"class" : "kikosPopup-poco-klaviyo"}, null, document.body);
            document.querySelector(".kikosPopup-poco-klaviyo").innerHTML = ps.html;
            let poco_popup_wrapper_style = document.createElement("style");
            document.body.append(poco_popup_wrapper_style);
            poco_popup_wrapper_style.innerHTML = '.poco-popup-wrapper {align-self : center; margin-left : auto; margin-right : auto;}';
            
            setupKikosPopup("kikosPopup-poco-klaviyo", ps);
        }
    }

    function setupKikosPopup (element_class_name, data) {
        var popup = new kikosPopup("." + element_class_name, {
            "width" : data.width,
            // "height" : data.height,
            "autoshow" : false,
            "overlay_opacity" : 0.6,
            "overlay_bgColor" : "#000000"
        });

        dobPicker({
            daySelector: "#dobday",
            monthSelector: "#dobmonth",
            yearSelector: "#dobyear",
            dayDefault: "Day",
            monthDefault: "Month",
            yearDefault: "Year",
            minimumAge: 13,
            maximumAge: 100
        });

        document.querySelectorAll(".kikosPopup-poco-klaviyo .kikos-close-btn").forEach(function (el) {
            el.addEventListener("click", function () {
                popup.close();
            });
        });

        if (document.getElementById("poco-popup-newsletter-submit")) {
            var submitBtn = document.getElementById("poco-popup-newsletter-submit");
            submitBtn.addEventListener("click", function (e) {
                var firstNameRequired = 0;
                var lastNameRequired = 0;
                if (!submitBtn.closest('[data-template="' + id_popup + '"]')) {
                    if (document.getElementById("popuppoco_newsletter_name") && document.getElementById("popuppoco_newsletter_name").hasAttribute('required')) {
                        firstNameRequired = 1;
                    }
                    if (document.getElementById("popuppoco_newsletter_lname") && document.getElementById("popuppoco_newsletter_lname").hasAttribute('required')) {
                        lastNameRequired = 1;
                    }
                }
                poco_ajax(
                    kv_ajax_url,
                    "POST",
                    {
                        action: "KLSubscribe",
                        apiKey: pocoApiKey,
                        email: document.getElementById("popuppoco_newsletter_email").value,
                        name: (document.getElementById("popuppoco_newsletter_name") ? document.getElementById("popuppoco_newsletter_name").value : ""),
                        lname: (document.getElementById("popuppoco_newsletter_lname") ? document.getElementById("popuppoco_newsletter_lname").value : ""),
                        day: (document.getElementById("dobday") ? document.getElementById("dobday").value : ""),
                        month: (document.getElementById('dobmonth') ? document.getElementById('dobmonth').value : ""),
                        firstNameRequired: firstNameRequired,
                        lastNameRequired: lastNameRequired
                    },
                    function (response) {
                        if (response.error) {
                            if (response.hasOwnProperty("field_name")) {
                                let errors = document.querySelectorAll(".error-msg");
                                if (errors.length > 0) {
                                    errors.forEach(function (error) {
                                        error.remove();
                                    });
                                }
                                let error_msg = document.createElement("div");
                                error_msg.innerText = response.error;
                                error_msg.classList.add("error-msg");
                                error_msg.style.textAlign = "left";
                                if (submitBtn.closest('[data-template="3"]')) {
                                    error_msg.style.marginTop = "4px"
                                } else {
                                    error_msg.style.marginTop = "-12px";
                                    error_msg.style.marginBottom = "20px";
                                }
                                error_msg.style.fontSize = "11px";
                                error_msg.style.color = "#f00";
                                if (response.field_name === "popuppoco_newsletter_email") {
                                    error_msg.classList.add("popuppoco_newsletter_email-error");
                                    document.getElementById("popuppoco_newsletter_email").closest("li").append(error_msg);
                                } else if (response.field_name === "popuppoco_newsletter_name") {
                                    error_msg.classList.add("popuppoco_newsletter_name-error");
                                    document.getElementById("popuppoco_newsletter_name").closest("li").append(error_msg);
                                } else if (response.field_name === "popuppoco_newsletter_lname") {
                                    error_msg.classList.add("popuppoco_newsletter_lname-error");
                                    document.getElementById("popuppoco_newsletter_lname").closest("div").append(error_msg);
                                } else if (response.field_name === "dobday") {
                                    error_msg.classList.add("dobday-error");
                                    document.getElementById("dobday").closest("li").append(error_msg);
                                }
                            } else {
                                alert(response.error);
                            }
                        } else {
                            _learnq.push(["identify", {
                                "$email": document.getElementById("popuppoco_newsletter_email").value
                            }]);

                            document.querySelectorAll(".poco-popup-content").forEach(function (el) {
                                el.style.width = '100%'
                                el.innerHTML = '<h3 style="text-align:center;">' + response.message + '</h3>';
                            });

                            localStorage.setItem('poco_popup_subscribed', 1);

                            setTimeout(function(){
                                popup.close();
                            }, 10000);
                        }
                    }
                );
                return false;
            });
        }


        var popup_bg_image = document.getElementById("popup_bg_image");
        if (popup_bg_image) {
            popup_bg_image.addEventListener("load", function () {
                popup.open();
                localStorage.setItem('poco_popup', 1);
                sessionStorage.setItem('poco_popup', 1);
            });
        } else {
            popup.open();
            localStorage.setItem('poco_popup', 1);
            sessionStorage.setItem('poco_popup', 1);
        }
    }

    function KVTrackAddToCart (data) {
        if (!company_id) {
            return false;
        }
        if (poco_plan !== "advanced" && !isOrdersSyncActive) {
            return false;
        }

        if (document.querySelector('[data-hook="product-image"]')) {
            localStorage.setItem('kv_product_image_' + data.id, document.querySelector('[data-hook="product-image"]').src);
        }
        localStorage.setItem('kv_product_url_' + data.id, location.href.replace(window.location.search, ''));

        poco_ajax(
            kv_ajax_url,
            "GET",
            {
                "action" : "addToCart",
                "apiKey" : pocoApiKey,
                "id_cart": data.cartId
            },
            function (response) {
                if (!response) {
                    return;
                }

                _learnq.push(["track", "Added to Cart", {
                    "$value": response.value,
                    "AddedItemProductName": data.name,
                    "AddedItemProductID": data.id,
                    "AddedItemSKU": data.sku,
                    "AddedItemCategories": [data.category],
                    "AddedItemImageURL": response.AddedItemImageURL,
                    "AddedItemPrice": data.price,
                    "AddedItemQuantity": data.quantity,
                    "CheckoutURL": response.CheckoutURL,
                    "Items": response.items
                }]);
            }
        );
    }

    function KVTrackProduct (data) {
        if (!company_id) {
            return false;
        }
        var prImage = document.querySelector('[data-hook="product-image"]');
        if (!prImage && document.querySelector('[data-hook="responsive-gallery-media"]')) {
            prImage = document.querySelector('[data-hook="responsive-gallery-media"]').style.backgroundImage.slice(4, -1).replace(/"/g, "");
        } else if (prImage) {
            prImage = prImage.src;
        }

        var item = {
            "ProductName": data.name,
            "ProductID": data.productId,
            "SKU": data.sku,
            "ImageURL": (prImage ? prImage : null),
            "URL": location.href.replace(window.location.search, ''),
            "Price": data.price
        };

        window.kv_track_product = item;

        _learnq.push(["track", "Viewed Product", item]);
    }

    function KVTrackCheckout (data) {
        if (!company_id) {
            return false;
        }

        if (poco_plan !== "advanced" && !isOrdersSyncActive) {
            return false;
        }

        var items = [];
        var item_names = [];
        var categories = [];
        var total = 0;
        for (product in data.contents) {
            if (data.contents.hasOwnProperty(product)) {
                var kv_image_url = decodeURIComponent(localStorage.getItem('kv_product_image_' + data['contents'][product]['id']));
                var kv_product_url = decodeURIComponent(localStorage.getItem('kv_product_url_' + data['contents'][product]['id']));
                if (kv_image_url == 'undefined') {
                    kv_image_url = '';
                }
                if (kv_product_url == 'undefined') {
                    kv_product_url = '';
                }
                var item = {};
                item.ProductID = data['contents'][product]['id'];
                item.ProductName = data['contents'][product]['name'];
                item.Quantity = data['contents'][product]['quantity'];
                item.ItemPrice = data['contents'][product]['price'];
                item.RowTotal = data['contents'][product]['price'] * data['contents'][product]['quantity'];
                item.ProductCategories = [data['contents'][product]['category']];
                item.ImageURL = kv_image_url;
                item.ProductURL = kv_product_url;
                items.push(item);
                item_names.push(data['contents'][product]['name']);
                categories.push(data['contents'][product]['category']);

                total += data['contents'][product]['price'] * data['contents'][product]['quantity'];
            }
        }

        setTimeout(function () {
            _learnq.push(["track", "Started Checkout", {
                "$event_id": new Date().getTime(),
                "$value": total,
                "ItemNames": item_names,
                "CheckoutURL": location.href,
                "Categories": categories,
                "Items": items
           }]);
        }, 3000);
    }

    function KVTrackCheckoutCustom (data) {
        if (!company_id) {
            return false;
        }

        if (poco_plan !== "advanced" && !isOrdersSyncActive) {
            return false;
        }

        let vars = {};

        location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) { vars[key] = value; });

        if (vars.hasOwnProperty("appSectionParams")) {
            let appSectionParams = JSON.parse(decodeURIComponent(vars.appSectionParams));

            if (!appSectionParams.hasOwnProperty("cartId")) {
                return false;
            }

            poco_ajax(
                kv_ajax_url,
                "GET",
                {
                    "action" : "checkoutCustom",
                    "apiKey" : pocoApiKey,
                    "id_cart" : appSectionParams.cartId
                },
                function (response) {
                    if (!response) {
                        return false;
                    }

                    _learnq.push(['identify', {
                        '$email': response.email
                    }]);

                    setTimeout(function(){
                        _learnq.push(["track", "Started Checkout", response.data]);
                    }, 7000);
                }
            );
        }
    }

    function initKVTrackingScript () {
        // Use KV embedded script //
        var wix_default_custom_element = document.querySelector("wix-default-custom-element");
        if (wix_default_custom_element) {
            wix_default_custom_element.innerHTML = '<div class="' + wix_default_custom_element.getAttribute("class") + '"></div>';
        }

        if (company_id) {
            var script = document.createElement('script');
            script.src = 'https://static.klaviyo.com/onsite/js/klaviyo.js?company_id=' + company_id;
            script.async = true;
            script.type = 'text/javascript';
            document.head.appendChild(script);
        }
    }

    function kvTrackMember () {
        if (!company_id) {
            return false;
        }

        var member_api_url = 'https://' + window.location.hostname + '/_api/apps/current-member/' + kv_app_id;

        poco_ajax(
            member_api_url,
            "GET",
            {},
            function (data) {
                if (typeof data.member !== 'undefined' && typeof data.member.id !== 'undefined') {
                    var urlParam = poco_getURLParam(document.getElementById("poco-kl-script").src, "pocoApiKey");
                    if (!urlParam) {
                        return;
                    }

                    poco_ajax(
                        kv_ajax_url,
                        "GET",
                        {
                            "action" : "getMember",
                            "apiKey" : pocoApiKey,
                            "id_member" : data.member.id
                        },
                        function (member) {
                            if (typeof member.member_email !== 'undefined') {
                                _learnq.push(['identify', {
                                    '$email': member.member_email
                                }]);
                            }
                        }
                    );
                }
            }
        );
    }

    function initKV () {
        // console.log('poco_kl', poco_kl);
        window.wixDevelopersAnalytics.register(kv_app_id, function report(eventName, data) {
            // console.log('kvtracking', eventName);
            switch(eventName) {
                case "PageView":
                    if (data.pageNumber - 1 >= pages_number) {
                        requestAndDisplayPopup(pocoApiKey);
                    }
                    break;
                case "productPageLoaded":
                    KVTrackProduct(data);
                    break;
                case "AddToCart":
                    KVTrackAddToCart(data);
                    break;
                case "InitiateCheckout":
                    KVTrackCheckout(data);
                    break;
                case "CustomEvent":
                    if (data["eventAction"] == "Sign up Success" || data["eventAction"] == "Log in Success") {
                        kvTrackMember();
                    }
                    if (data.hasOwnProperty("eventAction") && data.eventAction === "Add Shipping Details") {
                        KVTrackCheckoutCustom(data);
                    }
                    break;
            }
        });
    }

    function createDOMElement (tagName, attributes, css, appendTo, append) {
        if (!tagName) {
            return false;
        }

        attributes = attributes || {};
        css = css || {};
        appendTo = appendTo || null;
        append = append || null;

        let elem = document.createElement(tagName);

        for (let i in attributes) {
            if (attributes.hasOwnProperty(i)) {
                attributes[i] && elem.setAttribute(i, attributes[i]);
            }
        }

        for (let i in css) {
            if (css.hasOwnProperty(i)) {
                css[i] && (elem.style[i] = css[i]);
            }
        }

        appendTo && appendTo.append(elem);

        if (append) {
            if (Array.isArray(append)) {
                append.forEach(function (append_elem) {
                    append_elem && (typeof append_elem === "string" ? elem.insertAdjacentHTML("beforeend", append_elem) : elem.append(append_elem));
                });
            } else if (typeof append === "function") {
                let append_func = append();
                if (Array.isArray(append_func)) {
                    append_func.forEach(function (append_elem) {
                        append_elem && (typeof append_elem === "string" ? elem.insertAdjacentHTML("beforeend", append_elem) : elem.append(append_elem));
                    });
                } else {
                    (typeof append_func === "string" ? elem.insertAdjacentHTML("beforeend", append_func) : elem.append(append_func))
                }
            } else {
                (typeof append === "string" ? elem.insertAdjacentHTML("beforeend", append) : elem.append(append))
            }
        }

        return elem;
    }

    function nl2br (str, is_xhtml) {
        if (typeof str === 'undefined' || str === null) {
            return '';
        }
        var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
        return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    }

    function poco_ajax (url, method, params, callback, async) {
        method = method || "GET";
        params = params || {};
        callback = callback || function () {};
        async = (typeof async !== "undefined" ? async : true);

        var xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                try {
                    callback(JSON.parse(this.responseText));;
                } catch {
                    return false;
                }
            }
        }

        if (method === "GET") {
            if (params) {
                var params_key_val_arr = [];
                for (var i in params) {
                    if (params.hasOwnProperty(i)) {
                        params_key_val_arr.push(i + "=" + params[i]);
                    }
                }
            }
            xhr.open(method, url + "?" + (params ? params_key_val_arr.join("&") : ""), async);
            xhr.send();
        } else if (method === "POST") {
            if (params) {
                var formData = new FormData();

                for (var i in params) {
                    if (params.hasOwnProperty(i)) {
                        formData.append(i, params[i]);
                    }
                }
            }
            xhr.open(method, url, async);
            xhr.send(params ? formData : null);
        }
    }

    function parseJson (str) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return false;
        }
    }

    function cleanJsonStr (str) {
        return JSON.parse(atob(html_entity_decode(str).trim().substr(1).slice(0, -1).replaceAll('\\', '')));
    }

    function html_entity_decode(string, quote_style) {
        // Convert all HTML entities to their applicable characters
        var histogram = {}, symbol = '', tmp_str = '', entity = '';
        tmp_str = string.toString();

        if (false === (histogram = get_html_translation_table('HTML_ENTITIES', quote_style))) {
            return false;
        }

        // &amp; must be the last character when decoding!
        delete(histogram['&']);
        histogram['&'] = '&amp;';

        for (symbol in histogram) {
            entity = histogram[symbol];
            tmp_str = tmp_str.split(entity).join(symbol);
        }

        return tmp_str;
    }

    function get_html_translation_table(table, quote_style) {  
        // Returns the internal translation table used by htmlspecialchars and htmlentities
        // *     example 1: get_html_translation_table('HTML_SPECIALCHARS');
        // *     returns 1: {'"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;'}
          
        var entities = {}, histogram = {}, decimal = 0, symbol = '';
        var constMappingTable = {}, constMappingQuoteStyle = {};
        var useTable = {}, useQuoteStyle = {};
          
        useTable      = (table ? table.toUpperCase() : 'HTML_SPECIALCHARS');
        useQuoteStyle = (quote_style ? quote_style.toUpperCase() : 'ENT_COMPAT');
          
        // Translate arguments  
        constMappingTable[0]      = 'HTML_SPECIALCHARS';
        constMappingTable[1]      = 'HTML_ENTITIES';
        constMappingQuoteStyle[0] = 'ENT_NOQUOTES';
        constMappingQuoteStyle[2] = 'ENT_COMPAT';
        constMappingQuoteStyle[3] = 'ENT_QUOTES';
          
        // Map numbers to strings for compatibilty with PHP constants
        if (!isNaN(useTable)) {
            useTable = constMappingTable[useTable];
        }  
        if (!isNaN(useQuoteStyle)) {
            useQuoteStyle = constMappingQuoteStyle[useQuoteStyle];
        }
          
        if (useQuoteStyle != 'ENT_NOQUOTES') {
            entities['34'] = '&quot;';
        }  
      
        if (useQuoteStyle == 'ENT_QUOTES') {
            entities['39'] = '&#039;';
        }  
      
        if (useTable == 'HTML_SPECIALCHARS') {
            // ascii decimals for better compatibility
            entities['38'] = '&amp;';
            entities['60'] = '&lt;';
            entities['62'] = '&gt;';
        } else if (useTable == 'HTML_ENTITIES') {
            // ascii decimals for better compatibility
            entities['38']  = '&amp;';
            entities['60']  = '&lt;';
            entities['61']  = '&#61;';
            entities['62']  = '&gt;';
            entities['160'] = '&nbsp;';
            entities['161'] = '&iexcl;';
            entities['162'] = '&cent;';
            entities['163'] = '&pound;';
            entities['164'] = '&curren;';
            entities['165'] = '&yen;';
            entities['166'] = '&brvbar;';
            entities['167'] = '&sect;';
            entities['168'] = '&uml;';
            entities['169'] = '&copy;';
            entities['170'] = '&ordf;';
            entities['171'] = '&laquo;';
            entities['172'] = '&not;';
            entities['173'] = '&shy;';
            entities['174'] = '&reg;';
            entities['175'] = '&macr;';
            entities['176'] = '&deg;';
            entities['177'] = '&plusmn;';
            entities['178'] = '&sup2;';
            entities['179'] = '&sup3;';
            entities['180'] = '&acute;';
            entities['181'] = '&micro;';
            entities['182'] = '&para;';
            entities['183'] = '&middot;';
            entities['184'] = '&cedil;';
            entities['185'] = '&sup1;';
            entities['186'] = '&ordm;';
            entities['187'] = '&raquo;';
            entities['188'] = '&frac14;';
            entities['189'] = '&frac12;';
            entities['190'] = '&frac34;';
            entities['191'] = '&iquest;';
            entities['192'] = '&Agrave;';
            entities['193'] = '&Aacute;';
            entities['194'] = '&Acirc;';
            entities['195'] = '&Atilde;';
            entities['196'] = '&Auml;';
            entities['197'] = '&Aring;';
            entities['198'] = '&AElig;';
            entities['199'] = '&Ccedil;';
            entities['200'] = '&Egrave;';
            entities['201'] = '&Eacute;';
            entities['202'] = '&Ecirc;';
            entities['203'] = '&Euml;';
            entities['204'] = '&Igrave;';
            entities['205'] = '&Iacute;';
            entities['206'] = '&Icirc;';
            entities['207'] = '&Iuml;';
            entities['208'] = '&ETH;';
            entities['209'] = '&Ntilde;';
            entities['210'] = '&Ograve;';
            entities['211'] = '&Oacute;';
            entities['212'] = '&Ocirc;';
            entities['213'] = '&Otilde;';
            entities['214'] = '&Ouml;';
            entities['215'] = '&times;';
            entities['216'] = '&Oslash;';
            entities['217'] = '&Ugrave;';
            entities['218'] = '&Uacute;';
            entities['219'] = '&Ucirc;';
            entities['220'] = '&Uuml;';
            entities['221'] = '&Yacute;';
            entities['222'] = '&THORN;';
            entities['223'] = '&szlig;';
            entities['224'] = '&agrave;';
            entities['225'] = '&aacute;';
            entities['226'] = '&acirc;';
            entities['227'] = '&atilde;';
            entities['228'] = '&auml;';
            entities['229'] = '&aring;';
            entities['230'] = '&aelig;';
            entities['231'] = '&ccedil;';
            entities['232'] = '&egrave;';
            entities['233'] = '&eacute;';
            entities['234'] = '&ecirc;';
            entities['235'] = '&euml;';
            entities['236'] = '&igrave;';
            entities['237'] = '&iacute;';
            entities['238'] = '&icirc;';
            entities['239'] = '&iuml;';
            entities['240'] = '&eth;';
            entities['241'] = '&ntilde;';
            entities['242'] = '&ograve;';
            entities['243'] = '&oacute;';
            entities['244'] = '&ocirc;';
            entities['245'] = '&otilde;';
            entities['246'] = '&ouml;';
            entities['247'] = '&divide;';
            entities['248'] = '&oslash;';
            entities['249'] = '&ugrave;';
            entities['250'] = '&uacute;';
            entities['251'] = '&ucirc;';
            entities['252'] = '&uuml;';
            entities['253'] = '&yacute;';
            entities['254'] = '&thorn;';
            entities['255'] = '&yuml;';
        } else {
            throw Error("Table: "+useTable+' not supported');
            return false;
        }  

        // ascii decimals to real symbols
        for (decimal in entities) {
            symbol = String.fromCharCode(decimal);
            histogram[symbol] = entities[decimal];
        }

        return histogram;
    }
})();