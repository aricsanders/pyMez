<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 10/2016 Style sheet that maps VNA tools conn xml sheets to html-->

<!-- Template for entries-->

<xsl:template match='/'>

<html>
        <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>VNA Tools:<xsl:value-of select="//Identification"/></title>

    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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
</style>
</head>

<body>

  <!-- Tab Navigation -->
  <ul class="tab">
  <li><a href="#" class="tablinks" onclick="openTab(event, 'description')">Description</a></li>
  <li><a href="#" class="tablinks" onclick="openTab(event, 'plots')">Plots</a></li>
  <li><a href="#" class="tablinks" onclick="openTab(event, 'table')">Table</a></li>
  </ul>
  <!-- Description Page -->
  <div id="description" class="tabcontent">
	<h3>Cable Description:</h3>
    <br/><hr/>
		 <table id="DataDescription">
            <xsl:for-each select="Cable/*">
            <xsl:if test=".!='' and name()!='Zr' and name()!='ElectricalSpecifications'">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>

            <xsl:if test="name()='Zr'">
            <tr><th><b><xsl:value-of select="name()"/>:</b></th><td>
                <xsl:value-of select="./Real/Value"/> + <xsl:value-of select="./Imag/Value"/>j</td></tr>
            </xsl:if> 
            </xsl:for-each>
         </table>
    </div>
<!-- Plots -->
  <div id="plots" class="tabcontent">
    <h3>Data Plots:</h3>
    <table>
        <td>
        <button id="stabilityMagPlotToggleButton" type="button" class="btn btn-primary">Stability Magnitude</button>
        </td>
        <td>
        <button id="stabilityPhasePlotToggleButton" type="button" class="btn btn-primary">Stability Phase</button>
        </td>

    </table>
    <table>
        <tr>
            <td>
        <div id="stabilityMagPlot" style="width: 1000px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>

        </tr>
        <tr>
            <td>
        <div id="stabilityPhasePlot" style="width: 1000px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>

        </tr>

</table>
    </div>
<!-- Tabular Data -->
    <div id="table" class="tabcontent">
        <h3>Data:</h3>
        <table>
        <td>
        <button id="stabilityTableToggleButton" type="button" class="btn btn-primary">Show stability Table</button>
        </td>
        </table>
        <br/><hr/>
        <h3>stability</h3>

		<table class='table table-hover table-condensed table-bordered table-responsive' id="stabilityTable">
		    <tr>
            <xsl:for-each select="//Cable/ElectricalSpecifications/CableElectricalSpec[1]/*">

            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>

            </xsl:for-each>
            </tr>
            <xsl:for-each select="//Cable/ElectricalSpecifications/CableElectricalSpec">
            <tr>

            <xsl:for-each select="./*">

                <td><xsl:value-of select="."/></td>

		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
        <br/><hr/>

    </div>




<!-- Plotly Plot Scripts -->
<script>
    // stability Data
    var stabilityFrequency=[<xsl:for-each select="//Cable/ElectricalSpecifications/CableElectricalSpec/Frequency">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var stabilityMag=[<xsl:for-each select="//Cable/ElectricalSpecifications/CableElectricalSpec/StabilityMag">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var stabilityPhase=[<xsl:for-each select="//Cable/ElectricalSpecifications/CableElectricalSpec/StabilityPhase">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var stabilityMagPlotData =   {
    x: stabilityFrequency,
    y: stabilityMag,
    type: 'scatter',
    mode:'markers+lines',
    name:'stability '
  };
    var stabilityPhasePlotData =   {
    x: stabilityFrequency,
    y: stabilityPhase,
    type: 'scatter',
    mode:'markers+lines',
    name:'stability '
  };
  var stabilityMagLayout = {
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
    title:'Frequency (Hz)'},
  title:'Magnitude Stability'
  };
  var stabilityPhaseLayout = {
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
    title:'Frequency (Hz)'},
  title:'Phase Stability'
  };

Plotly.newPlot('stabilityMagPlot', [stabilityMagPlotData],stabilityMagLayout);
Plotly.newPlot('stabilityPhasePlot', [stabilityPhasePlotData],stabilityPhaseLayout);

	</script>

<!-- Buttons Definition-->

<script>

// Buttons to show data
$(document).ready(function(){

    $('#stabilityTableToggleButton').click(function(){
    $('#stabilityTable').toggle();});

    $('#stabilityMagPlotToggleButton').click(function(){
    $('#stabilityMagPlot').toggle();});
    $('#stabilityPhasePlotToggleButton').click(function(){
    $('#stabilityPhasePlot').toggle();});

});

</script>
<!-- Function for handling tabs -->
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
openTab(event, 'description');
</script>]]>
</xsl:text>
    </body>
</html>

    </xsl:template>
</xsl:stylesheet>
