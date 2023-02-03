import pandas as pd
import matplotlib.pyplot as plt
import io
from flask import Response,request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, session, redirect
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vector
from pyspark.ml.feature import VectorAssembler
import base64

app = Flask(__name__)
@app.route('/')
def plot_png():
    sc = SparkSession.builder.getOrCreate()
    spark = SparkSession(sc)
    df = spark.read.format("csv").option("encoding", "BIG5").option("header", "true").option("inferSchema", "true").load("s3://s711083104/Preview_Data.csv")
    
    # extra for everyCol
    col = df.columns
    
    # first page
    dds = df.toPandas().head(10)
    
    # second page
    dataframe = df.toPandas().describe() 
    
    return render_template("index.html", tablecol = col, tabledf = [dds.to_html(classes = 'data')], tabledds= [dataframe.to_html(classes = 'data')])

@app.route('/result', methods = ["post"])
def chooseXY():
    img = io.BytesIO()
    plt.switch_backend('agg')
    sc = SparkSession.builder.getOrCreate()
    spark = SparkSession(sc)
    df = spark.read.format("csv").option("encoding", "BIG5").option("header", "true").option("inferSchema", "true").load("s3://s711083104/Preview_Data.csv")
    
    # extra for everyCol
    col = df.columns
    
    # first page
    dds = df.toPandas().head(10)
    
    # second page
    dataframe = df.toPandas().describe() 
    
    colx1 = request.values["x1"]
    colx2 = request.values["x2"]
    colx3 = request.values["x3"]
    coly = request.values["y"]
    
    assembler = VectorAssembler(inputCols=[colx1, colx2, colx3], outputCol='features')
    output = assembler.transform(df)
    finalDF = output.select("features", coly)
    trainData, testData = finalDF.randomSplit([0.7, 0.3])
    lm = LinearRegression(labelCol = coly)
    model = lm.fit(trainData)
    unlabeled = testData.select("features")
    pre = model.transform(unlabeled)
    res = model.evaluate(testData)
    
    # output
    data = res.predictions
    pre = data.toPandas().head(10)
    
    x = data.select("prediction").toPandas() ["prediction"].values.tolist()
    y = data.select(coly).toPandas() [coly].values.tolist()
    
    plt.plot(y, y, c="red")
    plt.scatter(x, y)
    plt.savefig(img, format="png")
    img.seek(0)
    
    # third page
    plot_url_re = base64.b64encode(img.getvalue()).decode()
    
    return render_template("index.html" ,tablecol = col, tabledf = [dds.to_html(classes = 'data')], tabledds= [dataframe.to_html(classes = 'data')], pre = [pre.to_html(classes = 'data')] ,plot_url_re =plot_url_re)
    


if __name__ == "__main__":
    app.debug = True
    app.run(host = "127.0.0.1", port = 5000)