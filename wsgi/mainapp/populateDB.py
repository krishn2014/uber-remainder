from apiapp import models


u = models.University(1, "national", "delhi", "mumbai")
institype = models.Institype(1 , "sample")
insticlass = models.Insticlass(1, "sample")

i1 = models.Institute(1, "institute of technology", university = u, city="delhi", state="delhi")
i2 = models.Institute(2, "institute of ultra technology", university = u, city="delhi", state="delhi")
i1.save()
i2.save()
