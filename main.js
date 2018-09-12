var displayed = 0;
var json;
$.ajax({
  type: "get",
  url: "http://127.0.0.1/getdata.php",
  success: function(response) {
    json = eval(response);
    for (item in json) {
      filename = json[item]["filename"];
      tag = json[item]["tag"];
      author = json[item]["author"];
      state = json[item]["state"];
      character = json[item]["character"];
      if (state == "tagged")
        div =
          '<div class="col s12 "><div class="card"><div class="card-image"><img src="e:/pixiv/' +
          filename +
          '"></div><div class="card-content"><label for="">author:' +
          author +
          '</label><br><label for="" class="character">character:' +
          character +
          '</label><br><label for="" class="tag">tag:' +
          tag +
          "</label><br></div></div></div>";
      else
        div =
          '<div class="col s12 "><div class="card"><div class="card-image"><img src="e:/pixiv/' +
          filename +
          '"></div><div class="card-content"><label for="" class="tag">' +
          state +
          "</label></div></div></div>";
      if (displayed % 3 == 0)
        $("#piccontainer1")[0].innerHTML =
          $("#piccontainer1")[0].innerHTML + div;
      else if (displayed % 3 == 1)
        $("#piccontainer2")[0].innerHTML =
          $("#piccontainer2")[0].innerHTML + div;
      else
        $("#piccontainer3")[0].innerHTML =
          $("#piccontainer3")[0].innerHTML + div;

      displayed++;
      if (displayed == 200) break;
    }
  }
});

$(window).scroll(function() {
  var scrollTop = $(this).scrollTop();
  var scrollHeight = $(document).height();
  var windowHeight = $(this).height();
  if (scrollTop + windowHeight > scrollHeight - 100) {
    var origin_displayed = displayed;
    for (item = displayed; item < origin_displayed + 100; item++) {
      filename = json[item]["filename"];
      tag = json[item]["tag"];
      author = json[item]["author"];
      state = json[item]["state"];
      character = json[item]["character"];
      if (state == "tagged")
        div =
          '<div class="col s12"><div class="card"><div class="card-image"><img src="e:/pixiv/' +
          filename +
          '"></div><div class="card-content"><label for="">author:' +
          author +
          '</label><br><label for="" class="character">character:' +
          character +
          '</label><br><label for="" class="tag">tag:' +
          tag +
          "</label><br></div></div></div>";
      else
        div =
          '<div class="col s12"><div class="card"><div class="card-image"><img src="e:/pixiv/' +
          filename +
          '"></div><div class="card-content"><label for="" class="tag">' +
          state +
          "</label></div></div></div>";
      if (displayed % 3 == 0)
        $("#piccontainer1")[0].innerHTML =
          $("#piccontainer1")[0].innerHTML + div;
      else if (displayed % 3 == 1)
        $("#piccontainer2")[0].innerHTML =
          $("#piccontainer2")[0].innerHTML + div;
      else
        $("#piccontainer3")[0].innerHTML =
          $("#piccontainer3")[0].innerHTML + div;

      displayed++;
    }
  }
});

$("#search").bind("input", function() {
  var q = $("#search").val();
  var arrayQ = q.split(',');
  //json = {};
  var jsontemp;
  for(item in arrayQ){
    $.ajax({
      type: "post",
      url: "http://127.0.0.1/search.php",
      data: { q: arrayQ[item] },
      success: function(response) {
        jsontemp = $.extend(jsontemp,eval(response));
        if(item != arrayQ.length - 1 )
          return;
        json = jsontemp;
        $("#piccontainer1")[0].innerHTML = "";
        $("#piccontainer2")[0].innerHTML = "";
        $("#piccontainer3")[0].innerHTML = "";
        displayed = 0;
        for (item in json) {
          filename = json[item]["filename"];
          tag = json[item]["tag"];
          author = json[item]["author"];
          state = json[item]["state"];
          character = json[item]["character"];
          if (state == "tagged")
            div =
              '<div class="col s12 "><div class="card"><div class="card-image"><img src="e:/pixiv/' +
              filename +
              '"></div><div class="card-content"><label for="" class="author">author:' +
              author +
              '</label><br><label for="" class="character">character:' +
              character +
              '</label><br><label for="" class="tag">tag:' +
              tag +
              "</label><br></div></div></div>";
          else
            div =
              '<div class="col s12 "><div class="card"><div class="card-image"><img src="e:/pixiv/' +
              filename +
              '"></div><div class="card-content"><label for="" class="tag">' +
              state +
              "</label></div></div></div>";
          if (displayed % 3 == 0)
            $("#piccontainer1")[0].innerHTML =
              $("#piccontainer1")[0].innerHTML + div;
          else if (displayed % 3 == 1)
            $("#piccontainer2")[0].innerHTML =
              $("#piccontainer2")[0].innerHTML + div;
          else
            $("#piccontainer3")[0].innerHTML =
              $("#piccontainer3")[0].innerHTML + div;
  
          displayed++;
          if (displayed == 200) break;
        }
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        alert(XMLHttpRequest.status);
        alert(XMLHttpRequest.readyState);
        alert(textStatus);
      }
    });
  }
  
});
