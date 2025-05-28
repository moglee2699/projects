{{- define "orderservice.name" -}}
orderservice
{{- end -}}

{{- define "orderservice.fullname" -}}
{{- printf "%s-%s" .Release.Name "orderservice" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
