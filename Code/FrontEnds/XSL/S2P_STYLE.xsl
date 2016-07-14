<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 03/16/2016 Style sheet that maps S2P xml sheets to html-->

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
        <div id="reS11" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="imS11" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
        <tr>
            <td>
        <div id="reS21" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="imS21" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
        <tr>
            <td>
        <div id="reS22" style="width: 480px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        <td><div id="imS22" style="width: 480px; height: 400px;" class="plot">
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
    var reS11 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@reS11"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers'
  }
];
        var imS11 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@imS11"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
       mode:'markers'
  }
];
var reS11Layout = {
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
  title:'reS11'
};

    var imS11Layout = {
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
  title:'imS11'
};
    var reS22 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@reS22"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers'
  }
];
        var imS22 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@imS22"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
       mode:'markers'
  }
];
var reS22Layout = {
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
  title:'reS22'
};

    var imS22Layout = {
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
  title:'imS22'
};
    var reS21 =
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@reS21"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers',
    name:'S21'
  };
        var imS21 =
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@imS21"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
    mode:'markers',
    name:'S21'
  };

    var reS12 =
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@reS21"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers',
    name:'S12'
  };
        var imS12 =
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@imS21"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
    mode:'markers',
    name:'S12'
  };

var reS21Layout = {
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
  title:'reS21'
};

    var imS21Layout = {
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
  title:'imS21'
};
Plotly.newPlot('reS11', reS11,reS11Layout);
Plotly.newPlot('imS11', imS11,imS11Layout);
Plotly.newPlot('reS21', [reS21,reS12],reS21Layout);
Plotly.newPlot('imS21', [imS21,imS12],imS21Layout);
Plotly.newPlot('reS22', reS22,reS22Layout);
Plotly.newPlot('imS22', imS22,imS22Layout);
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
