from rest_framework import serializers
from django.db import transaction
from django.db.models import Max

import csv
import io

from .models import Course, Subject, Module, Syllabus, Batch
from apps.training.serializers import WeightageDistributionSerializer
from .constants import SubjectMethod


# -----------------------
# Subject
# -----------------------
class SubjectSerializer(serializers.ModelSerializer):
    weightage_distribution = WeightageDistributionSerializer(read_only=True)
    file = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = Subject
        fields = "__all__"

    def validate_code(self, value):
        if not value:
            return value

        queryset = Subject.objects.filter(code=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("This subject code already exists.")

        return value

    def create(self, validated_data):
        file = validated_data.pop("file", None)
    
        module_id = validated_data.get("module")
    
        # -------------------------
        # SINGLE CREATE
        # -------------------------
        if not file:
            try:
                return Subject.objects.create(**validated_data)
            except Exception as e:
                raise serializers.ValidationError({
                    "subject": f"Single create failed: {str(e)}"
                })
    
        # -------------------------
        # MODULE VALIDATION
        # -------------------------
        try:
            module = None
            if module_id:
                module = Module.objects.get(
                    pk=module_id.pk if hasattr(module_id, "pk") else module_id
                )
        except Module.DoesNotExist:
            raise serializers.ValidationError({
                "module": "Invalid module id"
            })
        except Exception as e:
            raise serializers.ValidationError({
                "module": str(e)
            })
    
        # -------------------------
        # CSV READ
        # -------------------------
        try:
            decoded_file = file.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(decoded_file))
        except Exception as e:
            raise serializers.ValidationError({
                "file": f"CSV read error: {str(e)}"
            })
    
        if not reader.fieldnames:
            raise serializers.ValidationError({
                "file": "CSV header missing or invalid"
            })
    
        # -------------------------
        # GET LAST CODE (SAFE)
        # -------------------------
        try:
            last_code = Subject.objects.filter(
                module=module
            ).aggregate(Max("code"))["code__max"]
    
            next_code = int(last_code) + 1 if last_code else 2001
    
        except Exception:
            next_code = 2001
    
        # -------------------------
        # BUILD SUBJECT LIST
        # -------------------------
        subjects = []
    
        try:
            for row_num, row in enumerate(reader, start=2):
    
                name = (row.get("name") or "").strip()
    
                if not name:
                    raise serializers.ValidationError({
                        "file": f"Row {row_num}: name is required"
                    })
    
                method = row.get("method")
    
                subjects.append(
                    Subject(
                        batch = module.batch if module else None,
                        module=module,
                        name=name,
                        code=str(next_code),
                        note=(row.get("note") or "").strip(),
    
                        written_mark=row.get("written_mark") or 0,
                        practical_mark=row.get("practical_mark") or 0,
                        viva_mark=row.get("viva_mark") or 0,
    
                        lecture_period=row.get("lecture_period"),
                        practical_period=row.get("practical_period"),
                        written_period=row.get("written_period"),
                        other_period=row.get("other_period"),
    
                        credit=row.get("credit") or 0,
                        method=method if method in SubjectMethod.values else SubjectMethod.OTHER,
                    )
                )
    
                next_code += 1
    
        except Exception as e:
            raise serializers.ValidationError({
                "file": f"Row processing error: {str(e)}"
            })
    
        # -------------------------
        # BULK CREATE
        # -------------------------
        try:
            with transaction.atomic():
                created_subjects = Subject.objects.bulk_create(subjects)
    
        except Exception as e:
            raise serializers.ValidationError({
                "file": f"Database error: {str(e)}"
            })
    
        # -------------------------
        # RETURN
        # -------------------------
        return created_subjects[-1] if created_subjects else None


# -----------------------
# Syllabus
# -----------------------
class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = "__all__"


# -----------------------
# Module
# -----------------------
class ModuleSerializer(serializers.ModelSerializer):
    syllabus_blocks = SyllabusSerializer(many=True, read_only=True)
    module_subjects = SubjectSerializer(many=True, read_only=True)
    file = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = Module
        fields = "__all__"

    def validate_code(self, value):
        queryset = Module.objects.filter(code=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("This module code already exists.")

        return value

    def create(self, validated_data):
        file = validated_data.pop("file", None)
    
        # -------------------------
        # SINGLE CREATE
        # -------------------------
        if not file:
            return Module.objects.create(**validated_data)
    
        batch_id = validated_data.get("batch")
    
        # Validate batch
        batch = None
        if batch_id:
            try:
                batch = Batch.objects.get(
                    pk=batch_id.pk if hasattr(batch_id, "pk") else batch_id
                )
            except Batch.DoesNotExist:
                raise serializers.ValidationError({
                    "batch": "Invalid batch id."
                })
    
        # -------------------------
        # BULK CREATE
        # -------------------------
        decoded_file = file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded_file))
    
        if not reader.fieldnames:
            raise serializers.ValidationError({
                "file": "CSV file is invalid."
            })
    
        last_code = Module.objects.aggregate(Max("code"))["code__max"]
    
        try:
            next_code = int(last_code) + 1 if last_code else 1001
        except (TypeError, ValueError):
            next_code = 1001
    
        modules = []
    
        for row in reader:
            modules.append(
                Module(
                    batch=batch,
                    name=row.get("name"),
                    code=str(next_code),
                    trade=row.get("trade"),
                    note=row.get("note"),
                )
            )
            next_code += 1
    
        with transaction.atomic():
            created_modules = Module.objects.bulk_create(modules)
    
        # return model instance 
        return created_modules[-1] if created_modules else None
        
        

# -----------------------
# Batch
# -----------------------
class BatchSerializer(serializers.ModelSerializer):
    batch_subjects = SubjectSerializer(many=True, read_only=True)
    module_batches = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = "__all__"


# -----------------------
# Course
# -----------------------
class CourseSerializer(serializers.ModelSerializer):
    syllabus_blocks = SyllabusSerializer(many=True, read_only=True)
    batches = BatchSerializer(many=True, read_only=True)
    childrens = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_childrens(self, obj):
        return CourseSerializer(obj.children.all(), many=True).data