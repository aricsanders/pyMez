<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 08/11/2016 Style sheet that maps PowerRawModel xml sheets to html-->
<!--Try to add in tabs -->
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
}</style>

        </head>
    <body>

  <ul class="tab">
  <li><a href="#" class="tablinks" onclick="openTab(event, 'description')">Description</a></li>
  <li><a href="#" class="tablinks" onclick="openTab(event, 'plots')">Plots</a></li>
  <li><a href="#" class="tablinks" onclick="openTab(event, 'table')">Table</a></li>
  </ul>


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
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td><a><xsl:attribute name="href">
                <xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a></td></tr>
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
                <b>magS11</b>
            </th>
            <th >
                <b>uMaS11</b>
            </th>
            <th >
                <b>uMbS11</b>
            </th>
            <th >
                <b>uMdS11</b>
            </th>
            <th >
                <b>uMgS11</b>
            </th>
            <th >
                <b>argS11</b>
            </th>
            <th >
                <b>uAaS11</b>
            </th>
            <th >
                <b>uAbS11</b>
            </th>
            <th >
                <b>uAdS11</b>
            </th>
            <th >
                <b>uAgS11</b>
            </th>
            <th >
                <b>Efficency</b>
            </th>
            <th >
                <b>uEs</b>
            </th>
            <th >
                <b>uEc</b>
            </th>
            <th >
                <b>uEe</b>
            </th>
            <th >
                <b>Calibration_Factor</b>
            </th>
            <th >
                <b>uCs</b>
            </th>
            <th >
                <b>uCc</b>
            </th>
            <th >
                <b>uCe</b>
            </th>

            </tr>
            <xsl:for-each select="//Data/Tuple">
            <tr>
            <xsl:for-each select="./@Frequency">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>


            <xsl:for-each select="./@magS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uMaS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uMbS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uMdS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uMgS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>

            <xsl:for-each select="./@argS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uAaS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uAbS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uAdS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uAgS11">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Efficiency">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uEs">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uEc">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uEe">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@Calibration_Factor">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uCs">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uCc">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            <xsl:for-each select="./@uCe">
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
    error_y: {
      type: 'data',
      array: [<xsl:for-each select="//Data/Tuple/@uMgS11"><xsl:value-of select="."/>,</xsl:for-each>],
      visible: true,
        },
    type: 'scatter',
    mode:'markers+lines'
  }
];
        var argS11 = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@argS11"><xsl:value-of select="."/>,</xsl:for-each>],
    error_y: {
      type: 'data',
      array: [<xsl:for-each select="//Data/Tuple/@uAgS11"><xsl:value-of select="."/>,</xsl:for-each>],
      visible: true,
        },

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
        error_y: {
    type: 'data',
      array: [<xsl:for-each select="//Data/Tuple/@uEe"><xsl:value-of select="."/>,</xsl:for-each>],
      visible: true,
        },

    type: 'scatter',
    mode:'markers+lines'
  }
];
        var Calibration_Factor = [
  {
    x: [<xsl:for-each select="//Data/Tuple/@Frequency"><xsl:value-of select="."/>,</xsl:for-each>],
    y: [<xsl:for-each select="//Data/Tuple/@Calibration_Factor"><xsl:value-of select="."/>,</xsl:for-each>],
    error_y: {
    type: 'data',
      array: [<xsl:for-each select="//Data/Tuple/@uCe"><xsl:value-of select="."/>,</xsl:for-each>],
      visible: true,
        },

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
</script>]]>
        </xsl:text>
    </body>
</html>

    </xsl:template>
</xsl:stylesheet>
