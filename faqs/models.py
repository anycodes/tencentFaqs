from django.db import models

# Create your models here.
class QAData(models.Model):
    qid = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    remark = models.CharField(max_length=150, verbose_name="备注说明")

    class Meta:
        verbose_name = "问答数据"
        verbose_name_plural = verbose_name
        ordering = ["-qid"]

    def __str__(self):
        return self.question
