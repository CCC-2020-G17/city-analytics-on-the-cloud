function (doc) {
    if(doc.place !== null){
        emit([doc.db_timestamp,doc.place.name], 1);
      
    }else if (doc.geo){
        if(doc.geo.coordinates[0]>-35.3503 && doc.geo.coordinates[0]<-34.5002 && doc.geo.coordinates[1]>138.4356 && doc.geo.coordinates[1]<139.0440){
            emit([doc.db_timestamp,'Adelaide'], 1);
        }
        else if(doc.geo.coordinates[0]>-28.3640 && doc.geo.coordinates[0]<-26.4523 && doc.geo.coordinates[1]>152.0734 && doc.geo.coordinates[1]<153.5467){
            emit([doc.db_timestamp,'Brisbane'], 1);
        }
        else if(doc.geo.coordinates[0]>-38.5030 && doc.geo.coordinates[0]<-37.1751 && doc.geo.coordinates[1]>144.3336 && doc.geo.coordinates[1]<145.8784){
            emit([doc.db_timestamp,'Melbourne'], 1);
        }
        else if(doc.geo.coordinates[0]>-32.8019 && doc.geo.coordinates[0]<-31.4551 && doc.geo.coordinates[1]>115.4495 && doc.geo.coordinates[1]<116.4151){
            emit([doc.db_timestamp,'Perth'], 1);
        }
        else if(doc.geo.coordinates[0]>-34.3311 && doc.geo.coordinates[0]<-32.9960 && doc.geo.coordinates[1]>149.9719 && doc.geo.coordinates[1]<151.6305){
            emit([doc.db_timestamp,'Sydney'], 1);
        }
    }else{
        emit([doc.db_timestamp,"Missing"], 1);
    }
  }