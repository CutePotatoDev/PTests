$.fn.api.settings.api = {
    "login": "/jump",
    "answer": location.pathname
}

$.fn.api.settings.successTest = function(response) {
    if(response && response.status) {
        return response.status;
    }
    return false
}

$(document).ready(
    function() {
        $("#login_form").form({
            fields: {
                famname: {
                    identifier: "std_famname",
                    rules: [
                        {
                            type: "empty",
                            prompt: "Enter surname."
                        },
                        {
                            type: "regExp[/^[a-zA-Z]*$/]",
                            prompt: "Incorrect surname format."
                        }
                    ]
                },
                stdid: {
                    identifier: "std_id",
                    rules: [
                        {
                            type: "empty",
                            prompt: "Enter student ID number."
                        },
                        {
                            type: "exactLength[8]",
                            prompt: "Student ID must be {ruleValue} numbers long."
                        }
                    ]
                }
            }
        }).api({
            action: "login",
            method: "POST",
            serializeForm: true,
            onFailure: function(response) {
                $(".error.message ul").remove()

                if (typeof response.status === "undefined")
                    $(".error.message").append("<ul class='list'><li>Server unreachable.</li></list>").show()
                else
                    if (!response.status)
                        $(".error.message").append("<ul class='list'><li>"+ response.msg +"</li></list>").show()                
            },
            onSuccess: function (response) {
                $(".error.message ul").remove()
                window.location = "/test/"+ response.id
            }
        });


        $("#question").form({
            fields: {
                checkbox: {
                    identifier: "answer",
                    rules: [
                        {
                            type: "checked",
                            prompt: "Mark answer."
                        }
                    ]
                },
            }
        }).api({
            action: "answer",
            method: "POST",
            // serializeForm: true,
            data: {
                answer: -1
            },
            beforeSend: function(settings) {
                data = []

                $(this).find("input").each(function(){
                    if($(this).is(":checked")){
                        data.push($(this).data("id"))
                    }
                });

                // console.log(data)
                settings.data.answer = data
                return settings;
            },
            onFailure: function(response) {
                $(".error.message ul").remove()
                $(".error.message").append("<ul class='list'><li>Error on sending answer.</li></list>").show()                
            },
            onSuccess: function (response) {
                $(".error.message ul").remove()

                if(response.done == true){
                    $("div.ui.checkbox input").each(function(){
                        $(this).prop("checked", false)
                    })

                    location.reload()
                    return
                }

                $("#question_info div").text(response.idx +"/"+ $("#question_info div").text().split("/")[1])
                $("#test_msg div h4").text(response.question)

                $("div.ui.checkbox").each(function(idx){
                    $(this).children("input").prop("checked", false)
                    $(this).children("label").text(response.answers[idx])
                })

            }
        });


    }
);