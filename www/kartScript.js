//Henter informasjon fra databasen og fyller ut salkart.
//Erik Roede 2014

$(document).ready(function(){
    //phpcall
    var inndata = 0;
    function phpCall() {
        $.post("dbsearch.php", function(data) {
            populateTable(data);
        });
    };
    
    function populateTable(data) {
        dataArray = JSON.parse(data);
        // Iterer over data, fyll kart
        for (var i = 0; i < dataArray.length; i++) {
            var mnavn = dataArray[i].maskinnavn;
            var inntid = dataArray[i].inntidspunkt;
            var dprinter = dataArray[i].defaultprinter;
            var mnr = mnavn.slice(4); //hardkoding, men
            var feilkode = dataArray[i].pingerstatus;
            //alert(dataArray[i].kommentarer);

            if (dataArray[i].kommentarer != null) {
                feilkode = 'annet';
            } else if (feilkode == '-') {
                feilkode = 'ureg';
            } else if (feilkode == 'Ok') {
                feilkode = 'ok';
            } else {
                feilkode = 'av';
            }
            
            $('#' + mnr).attr("feil", feilkode);
            $('#' + mnr).attr("cellenr", i);

            //html-innhold
            var celleinnhold = mnr + '<table class = \"maskininfo\"><tr><td>' 
                             + inntid + '</td> </tr><td>' 
                             + feilkode + '</td>  <tr> </tr></table>';
            $('#' + mnr).html(celleinnhold);
        };
        window.data = dataArray;
    };
    
    function showTip(parentCell){
        // Lager tooltip, mye som kan legges til her
        var tip = $('.pop');
        tip.show();
        ppos = $('#' + parentCell).position();
        popy = ppos.top;
        popx = ppos.left+$('#' + parentCell).width();
        tip.css({
            position: "absolute",
            top: popy, 
            left: popx,
        });

        // Finn info: finn cellenummer
        var cellenr = $('#' + parentCell).attr("cellenr");
        var maskindata = window.data[cellenr]
        var pophtml = maskindata.maskinnavn 
                    + '<br>Adresse: ' + maskindata.ip 
                    + '<br>Sist innlogget: ' + maskindata.inntidspunkt 
                    + '<br>Default printer: ' + maskindata.defaultprinter 
                    + '<br>Status: ' + maskindata.pingerstatus 
                    + '<br>Sist installert: ' + maskindata.sistinst 
                    + '<br><input type = "button" value = "Se bruk"></input> - kommer';

        if (maskindata.kommentarer != null){
            pophtml = pophtml + '<br>Merknader: ' + maskindata.kommentarer;
        }

        tip.html(pophtml);
    }

    // Lukker tooltip
    function closeTip() {
        var tip = $('.pop');
        tip.hide();
    }

    // Åpner tooltip
    $('.maskin').click(function(cell) {
        showTip(this.id);
    });

    // Lukker tooltip når man trykker utenfor
    $(document).mouseup(function(event) {
        tip = $('.pop');
        if (!tip.is(event.target)) { 
        //&& tip.has(event.target).length==0){
            closeTip();
        }
    })

    phpCall();
})


