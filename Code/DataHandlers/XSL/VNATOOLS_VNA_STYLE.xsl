<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 10/2016 Style sheet that maps VNA tools vnadev xml sheets to html-->

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
	<h3>VNA Description:</h3>
    <br/><hr/>
		 <table id="DataDescription">
            <xsl:for-each select="VnaDevice/*">
            <xsl:if test=".!='' and name()!='Zr' and name()!='Noise' and
                    name()!='LinearityPowerLevels' and name()!='Linearity' and name()!='Drift'">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>

            <xsl:if test="name()='Zr'">
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td> <xsl:value-of select="./Real/Value"/> + <xsl:value-of select="./Imag/Value"/>j</td></tr>
            </xsl:if> 
            </xsl:for-each>
         </table>
    </div>
<!-- Plots -->
  <div id="plots" class="tabcontent">
    <h3>Data Plots:</h3>
    <table>
        <td>
        <button id="NoisePlotToggleButton" type="button" class="btn btn-primary">Noise</button>
        </td>
        <td>
        <button id="DriftPlotToggleButton" type="button" class="btn btn-primary">Drift</button>
        </td>
        <td>
        <button id="LinearityPlotToggleButton" type="button" class="btn btn-primary">Linearity</button>
        </td>
    </table>
    <table>
        <tr>
            <td>
        <div id="noise" style="width: 1000px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>

        </tr>
        <tr>
        <td><div id="drift" style="width: 1000px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>

        <tr>
            <td>
        <div id="linearity" style="width: 1000px; height: 400px;" class="plot">
        <!-- Plotly chart will be drawn inside this DIV --></div></td>
        </tr>
</table>
    </div>
<!-- Tabular Data -->
    <div id="table" class="tabcontent">
        <h3>Data:</h3>
        <table>
        <td>
        <button id="NoiseToggleButton" type="button" class="btn btn-primary">Show Noise Table</button>
        </td>
        <td>
        <button id="DriftToggleButton" type="button" class="btn btn-primary">Show Drift Table</button>
        </td>
        <td>
        <button id="LinearityToggleButton" type="button" class="btn btn-primary">Show Linearity Table</button>
        </td>
        </table>
        <br/><hr/>
        <h3>Noise</h3>

		<table class='table table-hover table-condensed table-bordered table-responsive' id="NoiseTable">
		    <tr>
            <xsl:for-each select="//VnaDevice/Noise/VnaNoiseElectricalSpec[1]/*">

            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>

            </xsl:for-each>
            </tr>
            <xsl:for-each select="//VnaDevice/Noise/VnaNoiseElectricalSpec">
            <tr>

            <xsl:for-each select="./*">

                <td><xsl:value-of select="."/></td>

		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
        <br/><hr/>
        <h3>Drift</h3>

		<table class='table table-hover table-condensed table-bordered table-responsive' id="DriftTable">
		    <tr>
            <xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec[1]/*">

            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>

            </xsl:for-each>
            </tr>
            <xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec">
            <tr>
            <xsl:for-each select="./*">
                <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
        <br/><hr/>
        <h3>Linearity</h3>
        <table class='table table-hover table-condensed table-bordered table-responsive' id="LinearityTable">
		    <tr>
            <xsl:for-each select="//VnaDevice/Linearity/VnaLinearityElectricalSpec[1]/*">
            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>
            </xsl:for-each>
            </tr>
            <xsl:for-each select="//VnaDevice/Linearity/VnaLinearityElectricalSpec">
            <tr>
            <xsl:for-each select="./*">
            <td><xsl:value-of select="."/></td>
		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
    </div>




<!-- Plotly Plot Scripts -->
<script>
    // Noise Data
    var noiseFrequency=[<xsl:for-each select="//VnaDevice/Noise/VnaNoiseElectricalSpec/Frequency">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var noiseFloor =   {
    x: noiseFrequency,
    y: [<xsl:for-each select="//VnaDevice/Noise/VnaNoiseElectricalSpec/NoiseFloor"><xsl:value-of select="."/>,</xsl:for-each>],
    type: 'scatter',
    mode:'markers+lines',
    name:'Noise Floor'
  };
        var magTraceNoise = {
    x: noiseFrequency,
    y: [<xsl:for-each select="//VnaDevice/Noise/VnaNoiseElectricalSpec/TraceNoiseMag"><xsl:value-of select="."/>,</xsl:for-each>],

    type: 'scatter',
       mode:'markers+lines',
    name:'Trace Noise Mag'
  };

  var noiseLayout = {
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
  title:'Noise'
  };
    // drift terms
    var driftFrequency=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/Frequency">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftSwitchTerms=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftSwitchTerm">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftDirectivity=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftDirectivity">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftTrackingMag=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftTrackingMag">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftTrackingPhase=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftTrackingPhase">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftSymmetryMag=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftSymmetryMag">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftSymmetryPhase=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftSymmetryPhase">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftMatch=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftMatch">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var driftIsolation=[<xsl:for-each select="//VnaDevice/Drift/VnaDriftElectricalSpec/DriftIsolation">
    <xsl:value-of select="."/>,</xsl:for-each>];

    // Drift Plot Definition
    var driftSwitchTermsPlotData = {
    x: driftFrequency,
    y: driftSwitchTerms,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Switch Terms'
    };
    var driftTrackingMagPlotData = {
    x: driftFrequency,
    y: driftTrackingMag,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Tracking Mag'
    };
    var driftSymmetryMagPlotData = {
    x: driftFrequency,
    y: driftSymmetryMag,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Symmetry Mag'
    };
    var driftDirectivityPlotData = {
    x: driftFrequency,
    y: driftDirectivity,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Directivity'
    };
    var driftMatchPlotData = {
    x: driftFrequency,
    y: driftMatch,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Match'
    };
    var driftIsolationPlotData = {
    x: driftFrequency,
    y: driftIsolation,
    type: 'scatter',
    mode:'markers+lines',
    name:'Drift Isolation'
    };

    var driftLayout = {
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
      title:'Drift'
    };
    // Linearity Terms
    var linearityPower = [<xsl:for-each select="//VnaDevice/LinearityPowerLevels/double">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var linearityFrequency = [<xsl:for-each select="//VnaDevice/Linearity/VnaLinearityElectricalSpec/Frequency">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var linearityMag = [<xsl:for-each select="//VnaDevice/Linearity/VnaLinearityElectricalSpec/LinearityMag/double">
    <xsl:value-of select="."/>,</xsl:for-each>];
    var linearityPhase = [<xsl:for-each select="//VnaDevice/Linearity/VnaLinearityElectricalSpec/LinearityPhase/double">
    <xsl:value-of select="."/>,</xsl:for-each>];

    console.log(linearityFrequency.length)
    console.log(linearityPower.length)
    // Should be a loop
    <xsl:text disable-output-escaping="yes" >
    <![CDATA[
        var linearityList=[];
        for(i=0;i<=linearityFrequency.length;i++){
        var linearityPlot = {
        x: linearityPower,
        y: linearityMag.slice(i*linearityPower.length,(i+1)*linearityPower.length),
        type: 'scatter',
        mode:'markers+lines',
        name:'Linearity at ' + linearityFrequency[i] +'Hz'
        }
    linearityList.push(linearityPlot);
    }
    ]]>
    </xsl:text>



    var linearityLayout = {
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
        title:'Power (dB)'},
      title:'Linearity'
    };


Plotly.newPlot('noise', [noiseFloor,magTraceNoise],noiseLayout);
Plotly.newPlot('drift', [driftSwitchTermsPlotData,driftTrackingMagPlotData,driftSymmetryMagPlotData,
    driftDirectivityPlotData,driftIsolationPlotData,driftMatchPlotData],driftLayout);
Plotly.newPlot('linearity', linearityList,linearityLayout);

	</script>

<!-- Buttons Definition-->

<script>

// Buttons to show data
$(document).ready(function(){

    $('#NoiseToggleButton').click(function(){
    $('#NoiseTable').toggle();});
    $('#DriftToggleButton').click(function(){
    $('#DriftTable').toggle();});
    $('#LinearityToggleButton').click(function(){
    $('#LinearityTable').toggle();});

    $('#NoisePlotToggleButton').click(function(){
    $('#noise').toggle();});
    $('#DriftPlotToggleButton').click(function(){
    $('#drift').toggle();});
    $('#LinearityPlotToggleButton').click(function(){
    $('#linearity').toggle();});
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
