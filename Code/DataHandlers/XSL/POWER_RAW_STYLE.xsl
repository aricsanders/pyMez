<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 08/11/2016 Style sheet that maps PowerRawModel xml sheets to html-->

<!-- Template for entries-->

<xsl:template match='/'>

<html>
        <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Two port measurement</title>

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
    <div id="description" class="tabcontent">
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
  <div id="plots" class="tabcontent">
        <h3>Data Plot:</h3>
     <button id="ToggleButtonPlot" type="button" class="btn btn-primary">Show Plots</button><br/><hr/>
    <table>
        <tr>
            <td>
        <div id="magS11" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="argS11" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>

        <tr>
            <td>
        <div id="Efficiency" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="Calibration_Factor" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
</table>
    </div>
    <div id="table" class="tabcontent">
        <h3>Data:</h3>
        <button id="ToggleButton" type="button" class="btn btn-primary">Show Table</button><br/><hr/>
		<table class='table table-hover table-condensed table-bordered table-responsive' id="DataTable">
		    <tr>
            <th >
                <b>Frequency</b>
            </th>
            <th >
                <b>Connection</b>
            </th>
            <th >
                <b>Direction</b>
            </th>
            <th >
                <b>magS11</b>
            </th>
            <th >
                <b>argS11</b>
            </th>
            <th >
                <b>Efficency</b>
            </th>
            <th >
                <b>Calibration_Factor</b>
            </th>


            </tr>
            <xsl:for-each select="//Data/Tuple">
            <tr>
            <xsl:for-each select="./@Frequency">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Connect">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Direction">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@magS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@argS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Efficiency">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Calibration_Factor">
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
    var magS11 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@magS11"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers'
  }
];
        var argS11 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@argS11"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
       mode:'markers+lines'
  }
];
var magS11Layout = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }

  },
    xaxis:{
    title:'Frequency (GHz)'},
  title:'magS11'
};

    var argS11Layout = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
    xaxis:{
    title:'Frequency (GHz)'},
  title:'argS11'
};
    var Efficiency = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@Efficiency"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers+lines'
  }
];
        var Calibration_Factor = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@Calibration_Factor"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
       mode:'markers+lines'
  }
];
var EfficiencyLayout = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }

  },
    xaxis:{
    title:'Frequency (GHz)'},
  title:'Efficiency'
};

    var Calibration_FactorLayout = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
    xaxis:{
    title:'Frequency (GHz)'},
  title:'Calibration_Factor'
};


Plotly.newPlot('magS11', magS11,magS11Layout);
Plotly.newPlot('argS11', argS11,argS11Layout);
Plotly.newPlot('Efficiency', Efficiency,EfficiencyLayout);
Plotly.newPlot('Calibration_Factor', Calibration_Factor,Calibration_FactorLayout);
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
