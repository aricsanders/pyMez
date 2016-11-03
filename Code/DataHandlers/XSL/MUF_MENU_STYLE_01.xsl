<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 10/2016 Style sheet that maps MUF xml menus to html-->
<!-- Template for entries-->
    <xsl:template match='/'>
    <html>
        <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>MUF Menu: <xsl:value-of select="name(/*)" /></title>
    <link rel="shortcut icon"  href="MonteCarlo.ico" />

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
    <style>
        h1,h2 {text-align: center }
        div {border-style: solid;
        padding:5px;
        margin:10px;}

        #menuStripDiv {border-style: solid;
             border-color: blue;}
        #textBoxDiv {border-style: solid;
             border-color: green;}
        #controlDiv {border-style: solid;
             border-color: green;}
        #attribute {font-weight:bold;}
        #control {font-weight:bold;}

    </style>

</head>
<body>
    <div>
    <h1> Microwave Uncertainty Framework Menu -  <em><xsl:value-of select="name(/*)" /></em>  </h1>
    <table class='table table-hover table-condensed table-bordered table-responsive'>
            <xsl:for-each select="/*/@*">
                <tr>
                <td><span id="attribute"><xsl:value-of select="name()"/></span> :</td>
                <td><xsl:value-of select="."/></td>
                </tr>
            </xsl:for-each>
    </table>
    </div>
    <xsl:apply-templates/>

    </body>
    </html>
</xsl:template>
    <xsl:template match="//MenuStripItems">
        <div id="menuStripDiv">
            <h2>Menu Check Boxes</h2>
        <table class='table table-hover table-condensed table-bordered table-responsive'>
            <tr>
                <th>
                    Menu Item
                </th>
                <th>
                    Enabled
                </th>
                <th>
                    Checked
                </th>
            </tr>

            <xsl:for-each select="./*">
                <tr>
                <td>
                    <xsl:value-of select="name()"></xsl:value-of>
                </td>
                <td>
                    <xsl:value-of select="@Enabled"></xsl:value-of>
                </td>
                <td>
                    <xsl:value-of select="@Checked"></xsl:value-of>
                </td>
                </tr>
            </xsl:for-each>
            <tr>
            </tr>
        </table>
        </div>

    </xsl:template>
    <xsl:template match="//MenuStripTextBoxes">
        <div id="textBoxDiv">
            <h2> Menu Text Boxes </h2>
        <table class='table table-hover table-condensed table-bordered table-responsive'>
            <tr>
                <th>
                    Menu Item
                </th>
                <th>
                    Enabled
                </th>
                <th>
                    Text
                </th>
            </tr>
            <xsl:for-each select="./*">
                <tr>
                <td>
                    <xsl:value-of select="name()"></xsl:value-of>
                </td>
                <td>
                    <xsl:value-of select="@Enabled"></xsl:value-of>
                </td>
                <td>
                    <xsl:value-of select="@Text"></xsl:value-of>
                </td>
                </tr>
            </xsl:for-each>
            <tr>
            </tr>
        </table>
        </div>
    </xsl:template>

    <xsl:template match="//Controls/*">
    <div id="controlDiv">
    <h2> <span id="control">Control:</span> <xsl:value-of select="name()"/> </h2>
    <table border='true' class='table table-hover table-condensed table-bordered table-responsive'>
        <tr>
        <xsl:for-each select="./@*"><th><xsl:value-of select="name()"/></th></xsl:for-each>
        </tr>
        <tr>
        <xsl:for-each select="./@*">
        <td><xsl:value-of select="."/></td>
        </xsl:for-each>
        </tr>
    </table>
    <xsl:if test="@ControlType='System.Windows.Forms.ComboBox'">
    <select class="selectpicker">
        <xsl:for-each select="./Item">
        <option>
            <xsl:attribute name="value"><xsl:value-of select="@Index"/></xsl:attribute>
            <xsl:value-of select="@Text"/>
        </option>
        </xsl:for-each>
    </select>
    <table border='true' class='table table-hover table-condensed table-bordered table-responsive'>
        <tr>
        <xsl:for-each select="./Item[1]/@*"><th><xsl:value-of select="name()"/></th></xsl:for-each>
        </tr>
        <xsl:for-each select="./Item">
        <tr>
        <xsl:for-each select="./@*">
        <td><xsl:value-of select="."/></td>
            </xsl:for-each>
        </tr>
        </xsl:for-each>
    </table>
    </xsl:if>
    </div>
        <!--</xsl:if>-->
    </xsl:template>
    <xsl:template match="//FileMeasurement">
    <div id="fileMeasurementDiv">
    <br/><hr/>
     <span>Measurement</span>
     <br/><hr/>
    <table class='table table-hover table-condensed table-bordered table-responsive'>
            <xsl:for-each select="@*">
                <tr>
                <td><span id="attribute"><xsl:value-of select="name()"/></span> :</td>
                <td><xsl:value-of select="."/></td>
                </tr>
            </xsl:for-each>
    </table>


    </div>
        <!--</xsl:if>-->
    </xsl:template>
</xsl:stylesheet>
