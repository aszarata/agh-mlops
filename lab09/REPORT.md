# Raport
*Andrzej Szarata*

Do wykonania zadania został wykorzystany AWS Academy

## 2. Amazon S3 setup and file management
![zdjecie](images/report/1.png)
skrypt uploadujący dane znajduje się w folderze `scripts`.

## 3. Elastic Container Registry (ECR) & Docker management
![zdjecie](images/report/2.png)
ECR

![zdjecie](images/report/3.png)
Docker Image

## 4. Virtual Private Cloud (VPC) configuration
![zdjecie](images/report/4.png)
VPC

![zdjecie](images/report/5.png)
Subnety

![zdjecie](images/report/6.png)
Internet Gateway

![zdjecie](images/report/7.png)
![zdjecie](images/report/8.png)
Publiczny Routing Table

![zdjecie](images/report/9.png)
![zdjecie](images/report/10.png)
Prywatny Routing Table

![zdjecie](images/report/11.png)
![zdjecie](images/report/12.png)
Security groups

![zdjecie](images/report/23.png)
![zdjecie](images/report/22.png)
Resource Map

![zdjecie](images/report/13.png)
ALB target group


## 5. AWS Fargate deployment & CloudWatch configuration
![zdjecie](images/report/15.png)
Task definition

![zdjecie](images/report/16.png)
![zdjecie](images/report/17.png)
Cluster

## 6. Application testing and monitoring
Niestety miałem problem z load balancerem. Z jakiegoś powodu, przy jego tworzeniu wyświetlała się tylko jedna moliwość wyboru subneta podczas, gdy ALB mona było stworzyć tylko przy co najmniej dwóch subnetach (komunikat z ponizszego screena). Próbowałem na rózne sposoby, ale za nic nie dało się dodać drugiego. Później skończyła się moja sesja na AWS Academy.

Z tego powodu nie byłem w stanie połączyc się do endpointa...

![zdjecie](images/report/14.png)


Ponizej uruchomienie aplikacji lokalnie (jakiś dowód ze kontenery powinny działać, gdyby nie ten problem)
![zdjecie](images/report/19.png)
![zdjecie](images/report/20.png)
Sprawdzenie działania


