# Alitianchi-Guizhou-TravelTime-Prediction

### “数聚华夏 创享未来”中国数据创新行——智慧交通预测挑战赛


##### 比赛地址及其说明在[这里](https://tianchi.aliyun.com/competition/introduction.htm?spm=5176.100066.0.0.27d9fc3fci6mum&raceId=231598)

****
参赛成员

[张杰民](https://github.com/DB-jiemin) zjiemin.ai@gmail.com

[胡盛菁](https://github.com/Hushengjing) hsjarren@gmail.com

[杨双成](https://github.com/jackyang27) jackyyang1991@gmail.com


第一次参加数据科学类的比赛，排名在43/1716，三人初次合作都比较不易，但是经过这次比赛的磨合，期待在以后参加的比赛中获得更好的成绩~

看到github上有非常多优秀关于数据大赛的分享，我们打算也分享一下我们这次比赛的一些代码，算是对我们本次比赛的记录，如果大家发现在项目中有任何问题，欢迎写邮件向我们反馈，当然我们更是非常欢迎能有志同道合的朋友相互认识，相互学习，一起不断研究Machine learning & Deep learning

本文件中一共有三个文档，分别是:

* dataprocessing.py 
 
	对于时间信息的拆分，填补了缺失值，并对异常值进行清洗
* feature.py  


	计算了一些统计信息，包括一些周平均值等，更详细的信息请查看代码
* model.py

	运用了XGBoost和NN网络，并进行Ensemble