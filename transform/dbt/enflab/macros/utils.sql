{% macro is_empty_relation(relation) %}
  {% set sql %}
    SELECT 1 FROM {{ relation }} LIMIT 1
  {% endset %}
  {% set res = run_query(sql) %}
  {% if res and res.rows and res.rows[0][0] == 1 %}
    {{ return(False) }}
  {% endif %}
  {{ return(True) }}
{% endmacro %}
