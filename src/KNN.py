#-*-coding:utf-8 -*-
from sklearn import datasets  
#�����������ݼ�ģ��                      
from sklearn.neighbors import KNeighborsClassifier 
#����sklearn.neighborsģ����KNN��
import numpy as np
#Create branch T1
 
np.random.seed(0)  
#����������ӣ������õĻ�Ĭ���ǰ�ϵͳʱ����Ϊ���������ÿ�ε������ģ��ʱ���������������һ�����ú�ÿ�β�����һ��
iris=datasets.load_iris() 
#�����β�������ݼ���iris��һ�������ڽṹ��Ķ������ڲ����������ݣ�����Ǽලѧϰ���б�ǩ����
iris_x=iris.data   
#��������150*4��ά���ݣ�����150��������ÿ������4�����Էֱ�Ϊ����ͻ���ĳ�����
iris_y=iris.target  
#��150����Ϊ���飬�������ݵı�ǩ
indices = np.random.permutation(len(iris_x)) 
#permutation����һ������Ϊ����(150),����һ��0-149һά���飬ֻ������������ҵģ���Ȼ��Ҳ���Խ���һ��һά������Ϊ�����������ֱ�Ӷ�����������
iris_x_train = iris_x[indices[:-10]]
#���ѡȡ140��������Ϊѵ�����ݼ�
iris_y_train = iris_y[indices[:-10]] 
#����ѡȡ��140�������ı�ǩ��Ϊѵ�����ݼ��ı�ǩ
iris_x_test  = iris_x[indices[-10:]]
#ʣ�µ�10��������Ϊ�������ݼ�
iris_y_test  = iris_y[indices[-10:]] 
#���Ұ�ʣ��10��������Ӧ��ǩ��Ϊ�������ݼ��ı�ǩ

knn = KNeighborsClassifier() 
#����һ��knn����������
knn.fit(iris_x_train, iris_y_train)  
#���øö����ѵ����������Ҫ��������������ѵ�����ݼ�����������ǩ

iris_y_predict = knn.predict(iris_x_test) 
 #���øö���Ĳ��Է�������Ҫ����һ���������������ݼ�
probility=knn.predict_proba(iris_x_test)  
 #����������������ڸ��ʵ�Ԥ��
neighborpoint=knn.kneighbors(iris_x_test[-1],5,False)
#���������һ���������������������5���㣬���ص�����Щ�����������ɵ�����
score=knn.score(iris_x_test,iris_y_test,sample_weight=None)
#���øö���Ĵ�ַ����������׼ȷ��

print('iris_y_predict = ')  
print(iris_y_predict)  
#������ԵĽ��

print('iris_y_test = ')
print(iris_y_test)    
#���ԭʼ�������ݼ�����ȷ��ǩ���Է���Ա�
print ('Accuracy:',score)  
#���׼ȷ�ʼ�����
print ('neighborpoint of last test sample:',neighborpoint)
 
print ('probility:',probility)