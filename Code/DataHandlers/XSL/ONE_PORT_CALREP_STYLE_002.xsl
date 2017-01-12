<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 03/03/2016 Style sheet that maps one port xml sheets to html-->



<!-- Template for entries-->

<xsl:template match='/'>

<html>
        <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>One port measurement</title>

    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

<style> h3 {color:black}

ul.tab {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

/* Float the list items side by side */
ul.tab li {float: left;}

/* Style the links inside the list items */
ul.tab li a {
    display: inline-block;
    color: black;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
    transition: 0.3s;
    font-size: 17px;
}

/* Change background color of links on hover */
ul.tab li a:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
ul.tab li a:focus, .active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    display: none;
    padding: 6px 12px;
    -webkit-animation: fadeEffect 1s;
    animation: fadeEffect 1s;

}

@-webkit-keyframes fadeEffect {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes fadeEffect {
    from {opacity: 0;}
    to {opacity: 1;}
}
td {text-align:center}</style>

        </head>
    <body>
          <ul class="tab">
              <li><a href="#" class="tablinks" onclick="openTab(event, 'plots')">Plots</a></li>
              <li><a href="#" class="tablinks" onclick="openTab(event, 'description')">Description</a></li>
              <li><a href="#" class="tablinks" onclick="openTab(event, 'table')">Table</a></li>
  </ul>
    <div id="description" class="tabcontent">
		<h3>Data Description:</h3>
    <br/><hr/>
		 <table id="DataDescription">
            <xsl:for-each select="//Data_Description/*">
            <xsl:if test=".!='' and name()!='Instrument_Description'">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>

            <xsl:if test="name()='Instrument_Description'">
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td><a><xsl:attribute name="href"> <xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a></td></tr>
            </xsl:if> 
            </xsl:for-each>
         </table>
    </div>
    <div id="plots" class="tabcontent">
        <h3>Data Plot:</h3>
    <table>
        <tr>
            <td>
        <div id="plot" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div>
                <select id="axis-select" name="Axis Style">
                <option value="0">Linear x, Linear y</option>
                <option value="1">Linear x, Log y</option>
                <option value="2">Log x, Log y</option>
            </select>
            </td>
        <td><div id="error-plot" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
</table>
    </div>
    <div id="table" class="tabcontent">
        <h3>Data:</h3>
		<table class='table table-hover table-condensed table-bordered table-responsive' id="DataTable">
		    <tr>
            <xsl:for-each select="//Data/Tuple[1]/@*">
            
            <th ><b><xsl:value-of select="name()"/></b></th>
            
            </xsl:for-each>
            </tr>
            <xsl:for-each select="//Data/Tuple">
            <tr>
		    
            <xsl:for-each select="./@*">
         
                <td><xsl:value-of select="."/></td>
            
		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>
    function echo(object) {
    console.log(object);
    };
    function plotData(axisStyle){
    var frequency=[<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>];
    var yData=[<xsl:for-each select="//Data/Tuple/@magS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var yError=[<xsl:for-each select="//Data/Tuple/@uMgS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var argS11Data=[<xsl:for-each select="//Data/Tuple/@argS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var argS11Error=[<xsl:for-each select="//Data/Tuple/@uAgS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var upper=[];
    var lower=[];
    var argS11Upper=[];
    var argS11Lower=[];
    var xStyle="";
    var yStyle="";

    switch(axisStyle){
    case '0':
    yStyle='linear';
    xStyle='linear';
    break;
    case '1':
    yStyle='log';
    xStyle='linear';
    break;
    case '2':
    yStyle='log';
    xStyle='log';
    break;
    };
    echo(yStyle+" "+xStyle);
    <xsl:text disable-output-escaping="yes">
    <![CDATA[
    for(i=0;i<=yData.length;i++){
    upper.push(yData[i]+yError[i]);
    lower.push(yData[i]-yError[i]);
    argS11Upper.push(argS11Data[i]+argS11Error[i]);
    argS11Lower.push(argS11Data[i]-argS11Error[i]);
    };]]>
    </xsl:text>
    var magS11Upper={
    x:frequency ,
    y:upper,
    name:'S11+uMg',
    type: 'scatter',
    mode:'lines',
    line: {color: "rgb(0, 0, 255,.5)"},
  };
    var magS11Lower={
    x:frequency ,
    y:lower,
    name:'S11-uMg',
    type: 'scatter',
    mode:'lines',
    fill: "tonexty",
    fillcolor: "rgba(68, 68, 68, 0.3)",
    line: {color: "rgb(0, 0, 255,.5)"},
  };
    var magS11nitude = {
    x: frequency,
    y: yData,
    name:'S11',
    error_y: {
      type: 'data',
      array: yError,
      visible: false
    },
    type: 'scatter',
    mode:'lines',
    line: {color: "rgb(0, 0, 0,.5)",
    dash: 'dash',}
  };
        var phaseUpper={
    x:frequency ,
    y:argS11Upper,
    name:'phase+uAg',
    type: 'scatter',
    mode:'lines',
    line: {color: "rgb(0, 0, 255,.5)"},
  };
    var phaseLower={
    x:frequency ,
    y:argS11Lower,
    type: 'scatter',
    mode:'lines',
    name:'phase-uAg',
    fill: "tonexty",
    fillcolor: "rgba(68, 68, 68, 0.3)",
    line: {color: "rgb(0, 0, 255,.5)"},
  };
    var phase = {
    x: frequency,
    y: argS11Data,
    name:'phase',
    error_y: {
      type: 'data',
      array: argS11Error,
      visible: false,
    },
    type: 'scatter',
    mode:'lines'
  };
var magS11nitudeLayout = {
  legend: {y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey'
    }


  },
    showlegend: false,
    xaxis:{
    title:'Frequency (GHz)',
    type: xStyle},
    yaxis:{type: yStyle},
  title:'Magnitude'

};

    var phaseLayout = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
    showlegend:false,
    xaxis:{
    title:'Frequency (GHz)'},
  title:'Phase'
};

Plotly.newPlot('plot',[magS11Upper,magS11Lower,magS11nitude],magS11nitudeLayout);
Plotly.newPlot('error-plot', [phaseUpper,phaseLower,phase],phaseLayout);
    };
    plotData(0);
	</script>
<script>
    var axisSelector=document.getElementById('axis-select');
    axisSelector.addEventListener('change',function(){
    var axisValue=axisSelector.value;
    echo(axisValue);
    plotData(axisValue);
    }
    );
</script>
    <xsl:text disable-output-escaping="yes" >
        <![CDATA[<script>
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
openTab("","plots")
</script>]]>
        </xsl:text>
    </body>
</html>

    </xsl:template>
</xsl:stylesheet>
