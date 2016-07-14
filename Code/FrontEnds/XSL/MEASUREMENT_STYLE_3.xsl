<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 04/2010 Style sheet that maps measurement xml sheets to html-->



<!-- Template for entries-->

<xsl:template match='/'>
    
<html>
        <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Data Template</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet"/>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->






<style> h3 {color:black} </style>

        </head>






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
        <h3>Data Plot:</h3>
     <button id="ToggleButtonPlot" type="button" class="btn btn-primary">Show Plots</button><br/><hr/>
    <div id="plotS11" style="width: 480px; height: 400px;" class="plot"><!-- Plotly chart will be drawn inside this DIV --></div>
    <div id="plotS12" style="width: 480px; height: 400px;" class="plot"><!-- Plotly chart will be drawn inside this DIV --></div>
    <div id="plotS21" style="width: 480px; height: 400px;" class="plot"><!-- Plotly chart will be drawn inside this DIV --></div>
    <div id="plotS22" style="width: 480px; height: 400px;" class="plot"><!-- Plotly chart will be drawn inside this DIV --></div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

  <script>
   var traceS11 = {
  x: [<xsl:for-each select="//Data/Tuple/@Frequency">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  y: [<xsl:for-each select="//Data/Tuple/@Re_S11">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  type: 'scatter'
};
   var traceS12 = {
  x: [<xsl:for-each select="//Data/Tuple/@Frequency">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  y: [<xsl:for-each select="//Data/Tuple/@Re_S12">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  type: 'scatter'
};

      var traceS21 = {
  x: [<xsl:for-each select="//Data/Tuple/@Frequency">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  y: [<xsl:for-each select="//Data/Tuple/@Re_S21">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  type: 'scatter'
};


      var traceS22 = {
  x: [<xsl:for-each select="//Data/Tuple/@Frequency">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  y: [<xsl:for-each select="//Data/Tuple/@Re_S22">
                <xsl:value-of select="."/>,
            </xsl:for-each>],
  type: 'scatter'
};


      var dataS11 = [traceS11,traceS12,traceS22];
      var dataS12 = [traceS12];
      var dataS21 = [traceS21];
      var dataS22 = [traceS22];


      var layoutS11 ={
  title: 'Real S11',
  xaxis: {
    title: 'Frequency (GHz)'
  },
  yaxis: {
    title: 'Real S11'
  }
};
      var layoutS12 ={
  title: 'Real S12',
  xaxis: {
    title: 'Frequency (GHz)'
  },
  yaxis: {
    title: 'Real S12'
  }
};

      var layoutS21 ={
  title: 'Real S21',
  xaxis: {
    title: 'Frequency (GHz)'
  },
  yaxis: {
    title: 'Real S21'
  }
};

      var layoutS22 ={
  title: 'Real S21',
  xaxis: {
    title: 'Frequency (GHz)'
  },
  yaxis: {
    title: 'Real S21'
  }
};
      Plotly.newPlot('plotS11', dataS11, layoutS11);
      Plotly.newPlot('plotS12', dataS12, layoutS12);
      Plotly.newPlot('plotS21', dataS21, layoutS21);
      Plotly.newPlot('plotS22', dataS22, layoutS22);
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
