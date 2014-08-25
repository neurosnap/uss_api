(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-18083814-2', 'auto');
ga('send', 'pageview');

$.expr[':'].external = function(obj) {
    return !obj.href.match(/^mailto\:/)
        && (obj.hostname != location.hostname)
        && !obj.href.match(/^javascript\:/)
        && !obj.href.match(/^$/);
};

$(function() {
    $("a:external").each(function() {
        var link_text = $(this).html() + ' <span class="glyphicon glyphicon-new-window"></span>';
        $(this).html(link_text);
    });

    $('a:external').attr('target', '_blank');

    $(".json_format").on("click", function() {
        window.location.href = document.URL + "?format=json";
    });
});