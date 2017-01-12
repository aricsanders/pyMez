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


<style> h3 {color:black} </style>

        </head>
    <div>
		<h3>Data Description:</h3>
        <button id="ToggleButtonDescription" type="button" class="btn btn-primary">Show Description</button>
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
    <div>
        <h3>Data Plot:</h3>
     <button id="ToggleButtonPlot" type="button" class="btn btn-primary">Show Plots</button><br/><hr/>
    <table>
        <tr>
            <td>
        <div id="plot" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="error-plot" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
</table>
    </div>
    <div>
        <h3>Data:</h3>
        <button id="ToggleButton" type="button" class="btn btn-primary">Show Table</button><br/><hr/>
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
    var frequency=[<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>];
    var yData=[<xsl:for-each select="//Data/Tuple/@magS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var yError=[<xsl:for-each select="//Data/Tuple/@uMgS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var argS11Data=[<xsl:for-each select="//Data/Tuple/@argS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var argS11Error=[<xsl:for-each select="//Data/Tuple/@uAgS11"><xsl:value-of select="."/>,</xsl:for-each>];
    var upper=[]
    var lower=[]
    var argS11Upper=[]
    var argS11Lower=[]
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
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }


  },
    showlegend: false,
    xaxis:{
    title:'Frequency (GHz)'},
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
	</script>
    <script>
$(document).ready(function(){
    $("#ToggleButton").click(function(){
        $("#DataTable").toggle();});
        $("#ToggleButtonDescription").click(function(){
        $("#DataDescription").toggle();});
        $("#ToggleButtonPlot").click(function(){
        $(".plot").toggle();});


});
</script>
</html>

    </xsl:template>
</xsl:stylesheet>
