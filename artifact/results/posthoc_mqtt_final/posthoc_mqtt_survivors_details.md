# Post-hoc MQTT mutant classification

## sensor.py

### Mutant 15

- Class: **S2: MQTT payload/template handling**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_15.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -83,7 +83,7 @@\n-        and (state_class := config.get(CONF_STATE_CLASS)) != SensorStateClass.TOTAL\n+        and (state_class := config.get(CONF_STATE_CLASS)) == SensorStateClass.TOTAL
```

### Mutant 17

- Class: **S2: MQTT payload/template handling**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_17.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -86,7 +86,7 @@\n-            f"The option `{CONF_LAST_RESET_VALUE_TEMPLATE}` cannot be used "\n+            f"XXThe option `{CONF_LAST_RESET_VALUE_TEMPLATE}` cannot be used XX"
```

### Mutant 18

- Class: **S2: MQTT payload/template handling**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_18.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -87,7 +87,7 @@\n-            f"together with state class `{state_class}`"\n+            f"XXtogether with state class `{state_class}`XX"
```

### Mutant 20

- Class: **S3: MQTT state update**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_20.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -98,10 +98,7 @@\n-DISCOVERY_SCHEMA = vol.All(\n-    _PLATFORM_SCHEMA_BASE.extend({}, extra=vol.REMOVE_EXTRA),\n-    validate_sensor_state_class_config,\n-)\n+DISCOVERY_SCHEMA = None
```

### Mutant 27

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_27.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -128,7 +128,7 @@\n-    _expiration_trigger: CALLBACK_TYPE | None = None\n+    _expiration_trigger: CALLBACK_TYPE | None = ""
```

### Mutant 32

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_32.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -143,7 +143,7 @@\n-            (_expire_after := self._expire_after) is not None\n+            (_expire_after := self._expire_after) is  None
```

### Mutant 33

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_33.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -144,7 +144,7 @@\n-            and _expire_after > 0\n+            and _expire_after >= 0
```

### Mutant 34

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_34.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -144,7 +144,7 @@\n-            and _expire_after > 0\n+            and _expire_after > 1
```

### Mutant 35

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_35.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -145,7 +145,7 @@\n-            and (last_state := await self.async_get_last_state()) is not None\n+            and (last_state := await self.async_get_last_state()) is  None
```

### Mutant 36

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_36.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -146,7 +146,7 @@\n-            and last_state.state not in [STATE_UNKNOWN, STATE_UNAVAILABLE]\n+            and last_state.state  in [STATE_UNKNOWN, STATE_UNAVAILABLE]
```

### Mutant 37

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_37.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -148,7 +148,7 @@\n-            is not None\n+            is  None
```

### Mutant 38

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_38.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -151,7 +151,7 @@\n-            and not self._expiration_trigger\n+            and  self._expiration_trigger
```

### Mutant 39

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_39.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -143,8 +143,7 @@\n-            (_expire_after := self._expire_after) is not None\n-            and _expire_after > 0\n+            (_expire_after := self._expire_after) is not None or _expire_after > 0
```

### Mutant 40

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_40.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -153,7 +153,7 @@\n-            expiration_at = last_state.last_changed + timedelta(seconds=_expire_after)\n+            expiration_at = last_state.last_changed - timedelta(seconds=_expire_after)
```

### Mutant 41

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_41.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -153,7 +153,7 @@\n-            expiration_at = last_state.last_changed + timedelta(seconds=_expire_after)\n+            expiration_at = None
```

### Mutant 42

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_42.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -154,7 +154,7 @@\n-            remain_seconds = (expiration_at - dt_util.utcnow()).total_seconds()\n+            remain_seconds = (expiration_at + dt_util.utcnow()).total_seconds()
```

### Mutant 43

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_43.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -154,7 +154,7 @@\n-            remain_seconds = (expiration_at - dt_util.utcnow()).total_seconds()\n+            remain_seconds = None
```

### Mutant 44

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_44.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -156,7 +156,7 @@\n-            if remain_seconds <= 0:\n+            if remain_seconds < 0:
```

### Mutant 45

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_45.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -156,7 +156,7 @@\n-            if remain_seconds <= 0:\n+            if remain_seconds <= 1:
```

### Mutant 47

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_47.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -160,7 +160,7 @@\n-            self._expired = False\n+            self._expired = True
```

### Mutant 48

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_48.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -160,7 +160,7 @@\n-            self._expired = False\n+            self._expired = None
```

### Mutant 49

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_49.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -161,7 +161,7 @@\n-            self._attr_native_value = last_sensor_data.native_value\n+            self._attr_native_value = None
```

### Mutant 50

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_50.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -163,9 +163,7 @@\n-            self._expiration_trigger = async_call_later(\n-                self.hass, remain_seconds, self._value_is_expired\n-            )\n+            self._expiration_trigger = None
```

### Mutant 54

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_54.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -180,7 +180,7 @@\n-            self._expiration_trigger = None\n+            self._expiration_trigger = ""
```

### Mutant 65

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_65.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -200,7 +200,7 @@\n-        if self._expire_after is not None and self._expire_after > 0:\n+        if self._expire_after is not None and self._expire_after >= 0:
```

### Mutant 66

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_66.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -200,7 +200,7 @@\n-        if self._expire_after is not None and self._expire_after > 0:\n+        if self._expire_after is not None and self._expire_after > 1:
```

### Mutant 68

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_68.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -201,7 +201,7 @@\n-            self._expired = True\n+            self._expired = False
```

### Mutant 69

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_69.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -201,7 +201,7 @@\n-            self._expired = True\n+            self._expired = None
```

### Mutant 70

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_70.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -203,7 +203,7 @@\n-            self._expired = None\n+            self._expired = ""
```

### Mutant 78

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_78.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -220,7 +220,7 @@\n-            self._expired = False\n+            self._expired = True
```

### Mutant 79

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_79.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -220,7 +220,7 @@\n-            self._expired = False\n+            self._expired = None
```

### Mutant 80

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_80.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -227,9 +227,7 @@\n-            self._expiration_trigger = async_call_later(\n-                self.hass, self._expire_after, self._value_is_expired\n-            )\n+            self._expiration_trigger = None
```

### Mutant 82

- Class: **S2: MQTT payload/template handling**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_82.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -234,7 +234,7 @@\n-            payload = msg.payload\n+            payload = None
```

### Mutant 109

- Class: **S2: MQTT payload/template handling**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_109.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -279,7 +279,7 @@\n-            if last_reset is None:\n+            if last_reset is not None:
```

### Mutant 116

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_116.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -300,7 +300,7 @@\n-            {"_attr_native_value", "_attr_last_reset", "_expired"},\n+            {"_attr_native_value", "XX_attr_last_resetXX", "_expired"},
```

### Mutant 117

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_117.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -300,7 +300,7 @@\n-            {"_attr_native_value", "_attr_last_reset", "_expired"},\n+            {"_attr_native_value", "_attr_last_reset", "XX_expiredXX"},
```

### Mutant 123

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_123.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -319,6 +319,6 @@\n-            self._expire_after is None or not self._expired\n+            self._expire_after is not None or not self._expired
```

### Mutant 124

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_124.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -319,6 +319,6 @@\n-            self._expire_after is None or not self._expired\n+            self._expire_after is None or  self._expired
```

### Mutant 125

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_125.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -319,6 +319,6 @@\n-            self._expire_after is None or not self._expired\n+            self._expire_after is None and not self._expired
```

### Mutant 126

- Class: **S1: MQTT availability/expiration**
- Diff: `backups_resultados/sensor_antes_2h_20260702_1418/boofuzz/seed_1/mutant_diffs/mutant_126.diff`

```diff
--- ha_source/homeassistant/components/mqtt/sensor.py\n+++ ha_source/homeassistant/components/mqtt/sensor.py\n@@ -318,7 +318,7 @@\n-        return MqttAvailabilityMixin.available.fget(self) and (  # type: ignore[attr-defined]\n+        return MqttAvailabilityMixin.available.fget(self) or (  # type: ignore[attr-defined]
```

## template.py

### Mutant 15

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_15.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -103,7 +103,7 @@\n-    "contextfunction",\n+    "XXcontextfunctionXX",
```

### Mutant 16

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_16.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -104,7 +104,7 @@\n-    "evalcontextfunction",\n+    "XXevalcontextfunctionXX",
```

### Mutant 17

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_17.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -105,7 +105,7 @@\n-    "environmentfunction",\n+    "XXenvironmentfunctionXX",
```

### Mutant 18

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_18.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -106,7 +106,7 @@\n-    "jinja_pass_arg",\n+    "XXjinja_pass_argXX",
```

### Mutant 19

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_19.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -102,12 +102,7 @@\n-_RESERVED_NAMES = {\n-    "contextfunction",\n-    "evalcontextfunction",\n-    "environmentfunction",\n-    "jinja_pass_arg",\n-}\n+_RESERVED_NAMES = None
```

### Mutant 28

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_28.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -109,16 +109,7 @@\n-_COLLECTABLE_STATE_ATTRIBUTES = {\n-    "state",\n-    "attributes",\n-    "last_changed",\n-    "last_updated",\n-    "context",\n-    "domain",
```

### Mutant 29

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_29.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -120,7 +120,7 @@\n-ALL_STATES_RATE_LIMIT = 60  # seconds\n+ALL_STATES_RATE_LIMIT = 61  # seconds
```

### Mutant 30

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_30.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -120,7 +120,7 @@\n-ALL_STATES_RATE_LIMIT = 60  # seconds\n+ALL_STATES_RATE_LIMIT = None  # seconds
```

### Mutant 31

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_31.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -121,7 +121,7 @@\n-DOMAIN_STATES_RATE_LIMIT = 1  # seconds\n+DOMAIN_STATES_RATE_LIMIT = 2  # seconds
```

### Mutant 32

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_32.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -121,7 +121,7 @@\n-DOMAIN_STATES_RATE_LIMIT = 1  # seconds\n+DOMAIN_STATES_RATE_LIMIT = None  # seconds
```

### Mutant 33

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_33.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -123,7 +123,7 @@\n-_render_info: ContextVar[RenderInfo | None] = ContextVar("_render_info", default=None)\n+_render_info: ContextVar[RenderInfo & None] = ContextVar("_render_info", default=None)
```

### Mutant 34

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_34.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -123,7 +123,7 @@\n-_render_info: ContextVar[RenderInfo | None] = ContextVar("_render_info", default=None)\n+_render_info: ContextVar[RenderInfo | None] = ContextVar("XX_render_infoXX", default=None)
```

### Mutant 35

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_35.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -123,7 +123,7 @@\n-_render_info: ContextVar[RenderInfo | None] = ContextVar("_render_info", default=None)\n+_render_info: ContextVar[RenderInfo | None] = None
```

### Mutant 36

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_36.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -126,7 +126,7 @@\n-template_cv: ContextVar[tuple[str, str] | None] = ContextVar(\n+template_cv: ContextVar[tuple[str, str] & None] = ContextVar(
```

### Mutant 69

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_69.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -215,7 +215,7 @@\n-        obj.hass = hass\n+        obj.hass = None
```

### Mutant 70

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_70.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -221,7 +221,7 @@\n-    limited: bool = False,\n+    limited: bool = True,
```

### Mutant 71

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_71.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -222,7 +222,7 @@\n-    parse_result: bool = True,\n+    parse_result: bool = False,
```

### Mutant 72

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_72.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -245,7 +245,7 @@\n-        return True\n+        return False
```

### Mutant 73

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_73.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -249,7 +249,7 @@\n-        return any(is_complex(val) for val in value) or any(\n+        return any(is_complex(val) for val in value) and any(
```

### Mutant 74

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_74.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -252,7 +252,7 @@\n-    return False\n+    return True
```

### Mutant 77

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_77.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -258,7 +258,7 @@\n-        "{%" in maybe_template or "{{" in maybe_template or "{#" in maybe_template\n+        "XX{%XX" in maybe_template or "{{" in maybe_template or "{#" in maybe_template
```

### Mutant 78

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_78.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -258,7 +258,7 @@\n-        "{%" in maybe_template or "{{" in maybe_template or "{#" in maybe_template\n+        "{%" not in maybe_template or "{{" in maybe_template or "{#" in maybe_template
```

### Mutant 81

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_81.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -258,7 +258,7 @@\n-        "{%" in maybe_template or "{{" in maybe_template or "{#" in maybe_template\n+        "{%" in maybe_template or "{{" in maybe_template or "XX{#XX" in maybe_template
```

### Mutant 82

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_82.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -258,7 +258,7 @@\n-        "{%" in maybe_template or "{{" in maybe_template or "{#" in maybe_template\n+        "{%" in maybe_template or "{{" in maybe_template or "{#" not in maybe_template
```

### Mutant 84

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_84.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -257,7 +257,7 @@\n-    return "{" in maybe_template and (\n+    return "{" in maybe_template or (
```

### Mutant 85

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_85.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -276,7 +276,7 @@\n-            self.render_result = render_result\n+            self.render_result = None
```

### Mutant 86

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_86.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -279,7 +279,7 @@\n-            if self.render_result is None:\n+            if self.render_result is not None:
```

### Mutant 87

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_87.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -281,7 +281,7 @@\n-                if kls is set:\n+                if kls is not set:
```

### Mutant 89

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_89.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -304,7 +304,7 @@\n-        self.render_result = render_result\n+        self.render_result = None
```

### Mutant 90

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_90.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -308,7 +308,7 @@\n-        if self.render_result is None:\n+        if self.render_result is not None:
```

### Mutant 91

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_91.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -314,7 +314,7 @@\n-_types: tuple[type[dict | list | set], ...] = (dict, list, set)\n+_types: tuple[type[dict & list | set], ...] = (dict, list, set)
```

### Mutant 92

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_92.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -314,7 +314,7 @@\n-_types: tuple[type[dict | list | set], ...] = (dict, list, set)\n+_types: tuple[type[dict | list & set], ...] = (dict, list, set)
```

### Mutant 95

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_95.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -316,7 +316,7 @@\n-RESULT_WRAPPERS[tuple] = TupleWrapper\n+RESULT_WRAPPERS[tuple] = None
```

### Mutant 98

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_98.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -326,8 +326,6 @@\n-\n-@lru_cache(maxsize=EVAL_CACHE_SIZE)
```

### Mutant 99

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_99.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -330,7 +330,7 @@\n-    result = literal_eval(render_result)\n+    result = None
```

### Mutant 100

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_100.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -331,7 +331,7 @@\n-    if type(result) in RESULT_WRAPPERS:\n+    if type(result) not in RESULT_WRAPPERS:
```

### Mutant 101

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_101.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -332,7 +332,7 @@\n-        result = RESULT_WRAPPERS[type(result)](result, render_result=render_result)\n+        result = None
```

### Mutant 102

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_102.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -341,7 +341,7 @@\n-        not isinstance(result, (str, complex))\n+         isinstance(result, (str, complex))
```

### Mutant 103

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_103.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -344,7 +344,7 @@\n-            not isinstance(result, (int, float))\n+             isinstance(result, (int, float))
```

### Mutant 104

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_104.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -348,7 +348,7 @@\n-            or _IS_NUMERIC.match(render_result) is not None\n+            or _IS_NUMERIC.match(render_result) is  None
```

### Mutant 105

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_105.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -344,9 +344,7 @@\n-            not isinstance(result, (int, float))\n-            # Or it's a boolean (inherit from int)\n-            or isinstance(result, bool)\n+            not isinstance(result, (int, float)) and isinstance(result, bool)
```

### Mutant 106

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_106.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -341,8 +341,7 @@\n-        not isinstance(result, (str, complex))\n-        and (\n+        not isinstance(result, (str, complex)) or (
```

### Mutant 107

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_107.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -360,7 +360,7 @@\n-        "template",\n+        "XXtemplateXX",
```

### Mutant 108

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_108.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -361,7 +361,7 @@\n-        "filter_lifecycle",\n+        "XXfilter_lifecycleXX",
```

### Mutant 109

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_109.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -362,7 +362,7 @@\n-        "filter",\n+        "XXfilterXX",
```

### Mutant 110

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_110.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -363,7 +363,7 @@\n-        "_result",\n+        "XX_resultXX",
```

### Mutant 111

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_111.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -364,7 +364,7 @@\n-        "is_static",\n+        "XXis_staticXX",
```

### Mutant 122

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_122.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -379,7 +379,7 @@\n-        self.filter_lifecycle: Callable[[str], bool] = _true\n+        self.filter_lifecycle: Callable[[str], bool] = None
```

### Mutant 123

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_123.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -380,7 +380,7 @@\n-        self.filter: Callable[[str], bool] = _true\n+        self.filter: Callable[[str], bool] = None
```

### Mutant 124

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_124.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -381,7 +381,7 @@\n-        self._result: str | None = None\n+        self._result: str & None = None
```

### Mutant 125

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_125.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -381,7 +381,7 @@\n-        self._result: str | None = None\n+        self._result: str | None = ""
```

### Mutant 126

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_126.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -382,7 +382,7 @@\n-        self.is_static = False\n+        self.is_static = True
```

### Mutant 127

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_127.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -382,7 +382,7 @@\n-        self.is_static = False\n+        self.is_static = None
```

### Mutant 128

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_128.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -383,7 +383,7 @@\n-        self.exception: TemplateError | None = None\n+        self.exception: TemplateError & None = None
```

### Mutant 129

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_129.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -383,7 +383,7 @@\n-        self.exception: TemplateError | None = None\n+        self.exception: TemplateError | None = ""
```

### Mutant 130

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_130.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -384,7 +384,7 @@\n-        self.all_states = False\n+        self.all_states = True
```

### Mutant 131

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_131.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -384,7 +384,7 @@\n-        self.all_states = False\n+        self.all_states = None
```

### Mutant 132

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_132.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -385,7 +385,7 @@\n-        self.all_states_lifecycle = False\n+        self.all_states_lifecycle = True
```

### Mutant 133

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_133.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -385,7 +385,7 @@\n-        self.all_states_lifecycle = False\n+        self.all_states_lifecycle = None
```

### Mutant 134

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_134.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -386,7 +386,7 @@\n-        self.domains: collections.abc.Set[str] = set()\n+        self.domains: collections.abc.Set[str] = None
```

### Mutant 157

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_157.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -429,7 +429,7 @@\n-        return split_entity_id(entity_id)[0] in self.domains_lifecycle\n+        return split_entity_id(entity_id)[1] in self.domains_lifecycle
```

### Mutant 158

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_158.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -429,7 +429,7 @@\n-        return split_entity_id(entity_id)[0] in self.domains_lifecycle\n+        return split_entity_id(entity_id)[0] not in self.domains_lifecycle
```

### Mutant 159

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_159.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -433,7 +433,7 @@\n-        if self.exception is not None:\n+        if self.exception is  None:
```

### Mutant 160

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_160.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -438,7 +438,7 @@\n-        self.is_static = True\n+        self.is_static = False
```

### Mutant 161

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_161.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -438,7 +438,7 @@\n-        self.is_static = True\n+        self.is_static = None
```

### Mutant 194

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_194.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -500,7 +500,7 @@\n-        self._compiled_code: CodeType | None = None\n+        self._compiled_code: CodeType & None = None
```

### Mutant 196

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_196.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -501,7 +501,7 @@\n-        self._compiled: jinja2.Template | None = None\n+        self._compiled: jinja2.Template & None = None
```

### Mutant 197

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_197.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -501,7 +501,7 @@\n-        self._compiled: jinja2.Template | None = None\n+        self._compiled: jinja2.Template | None = ""
```

### Mutant 198

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_198.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -502,7 +502,7 @@\n-        self.hass = hass\n+        self.hass = None
```

### Mutant 200

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_200.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -503,7 +503,7 @@\n-        self.is_static = not is_template_string(template)\n+        self.is_static = None
```

### Mutant 201

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_201.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -504,7 +504,7 @@\n-        self._exc_info: sys._OptExcInfo | None = None\n+        self._exc_info: sys._OptExcInfo & None = None
```

### Mutant 202

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_202.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -504,7 +504,7 @@\n-        self._exc_info: sys._OptExcInfo | None = None\n+        self._exc_info: sys._OptExcInfo | None = ""
```

### Mutant 205

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_205.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -506,7 +506,7 @@\n-        self._strict: bool | None = None\n+        self._strict: bool & None = None
```

### Mutant 207

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_207.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -507,7 +507,7 @@\n-        self._log_fn: Callable[[int, str], None] | None = None\n+        self._log_fn: Callable[[int, str], None] & None = None
```

### Mutant 209

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_209.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -508,7 +508,7 @@\n-        self._hash_cache: int = hash(self.template)\n+        self._hash_cache: int = None
```

### Mutant 210

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_210.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -509,7 +509,7 @@\n-        self._renders: int = 0\n+        self._renders: int = 1
```

### Mutant 225

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_225.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -551,7 +551,7 @@\n-        parse_result: bool = True,\n+        parse_result: bool = False,
```

### Mutant 226

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_226.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -552,7 +552,7 @@\n-        limited: bool = False,\n+        limited: bool = True,
```

### Mutant 227

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_227.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -561,7 +561,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if  parse_result or self.hass and self.hass.config.legacy_templates:
```

### Mutant 228

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_228.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -561,7 +561,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if not parse_result or self.hass or self.hass.config.legacy_templates:
```

### Mutant 229

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_229.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -561,7 +561,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if not parse_result and self.hass and self.hass.config.legacy_templates:
```

### Mutant 230

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_230.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -564,7 +564,7 @@\n-        assert self.hass is not None, "hass variable not set on template"\n+        assert self.hass is  None, "hass variable not set on template"
```

### Mutant 232

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_232.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -570,7 +570,6 @@\n-    @callback
```

### Mutant 233

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_233.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -574,7 +574,7 @@\n-        parse_result: bool = True,\n+        parse_result: bool = False,
```

### Mutant 234

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_234.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -575,7 +575,7 @@\n-        limited: bool = False,\n+        limited: bool = True,
```

### Mutant 235

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_235.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -576,7 +576,7 @@\n-        strict: bool = False,\n+        strict: bool = True,
```

### Mutant 236

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_236.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -587,7 +587,7 @@\n-        self._renders += 1\n+        self._renders = 1
```

### Mutant 237

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_237.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -587,7 +587,7 @@\n-        self._renders += 1\n+        self._renders -= 1
```

### Mutant 238

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_238.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -587,7 +587,7 @@\n-        self._renders += 1\n+        self._renders += 2
```

### Mutant 239

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_239.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -590,7 +590,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if  parse_result or self.hass and self.hass.config.legacy_templates:
```

### Mutant 240

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_240.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -590,7 +590,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if not parse_result or self.hass or self.hass.config.legacy_templates:
```

### Mutant 241

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_241.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -590,7 +590,7 @@\n-            if not parse_result or self.hass and self.hass.config.legacy_templates:\n+            if not parse_result and self.hass and self.hass.config.legacy_templates:
```

### Mutant 242

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_242.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -594,7 +594,7 @@\n-        compiled = self._compiled or self._ensure_compiled(limited, strict, log_fn)\n+        compiled = self._compiled and self._ensure_compiled(limited, strict, log_fn)
```

### Mutant 243

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_243.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -594,7 +594,7 @@\n-        compiled = self._compiled or self._ensure_compiled(limited, strict, log_fn)\n+        compiled = None
```

### Mutant 244

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_244.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -596,7 +596,7 @@\n-        if variables is not None:\n+        if variables is  None:
```

### Mutant 245

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_245.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -600,7 +600,7 @@\n-            render_result = _render_with_context(self.template, compiled, **kwargs)\n+            render_result = None
```

### Mutant 246

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_246.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -604,7 +604,7 @@\n-        render_result = render_result.strip()\n+        render_result = None
```

### Mutant 247

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_247.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -606,7 +606,7 @@\n-        if not parse_result or self.hass and self.hass.config.legacy_templates:\n+        if  parse_result or self.hass and self.hass.config.legacy_templates:
```

### Mutant 248

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_248.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -606,7 +606,7 @@\n-        if not parse_result or self.hass and self.hass.config.legacy_templates:\n+        if not parse_result or self.hass or self.hass.config.legacy_templates:
```

### Mutant 249

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_249.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -606,7 +606,7 @@\n-        if not parse_result or self.hass and self.hass.config.legacy_templates:\n+        if not parse_result and self.hass and self.hass.config.legacy_templates:
```

### Mutant 250

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_250.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -624,7 +624,7 @@\n-        strict: bool = False,\n+        strict: bool = True,
```

### Mutant 251

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_251.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -641,7 +641,7 @@\n-        self._renders += 1\n+        self._renders = 1
```

### Mutant 252

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_252.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -641,7 +641,7 @@\n-        self._renders += 1\n+        self._renders -= 1
```

### Mutant 253

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_253.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -641,7 +641,7 @@\n-        self._renders += 1\n+        self._renders += 2
```

### Mutant 254

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_254.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -644,7 +644,7 @@\n-            return False\n+            return True
```

### Mutant 255

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_255.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -646,7 +646,7 @@\n-        compiled = self._compiled or self._ensure_compiled(strict=strict, log_fn=log_fn)\n+        compiled = self._compiled and self._ensure_compiled(strict=strict, log_fn=log_fn)
```

### Mutant 256

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_256.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -646,7 +646,7 @@\n-        compiled = self._compiled or self._ensure_compiled(strict=strict, log_fn=log_fn)\n+        compiled = None
```

### Mutant 257

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_257.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -648,7 +648,7 @@\n-        if variables is not None:\n+        if variables is  None:
```

### Mutant 258

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_258.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -651,7 +651,7 @@\n-        self._exc_info = None\n+        self._exc_info = ""
```

### Mutant 259

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_259.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -652,7 +652,7 @@\n-        finish_event = asyncio.Event()\n+        finish_event = None
```

### Mutant 260

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_260.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -655,7 +655,7 @@\n-            assert self.hass is not None, "hass variable not set on template"\n+            assert self.hass is  None, "hass variable not set on template"
```

### Mutant 263

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_263.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -666,7 +666,7 @@\n-            template_render_thread = ThreadWithException(target=_render_template)\n+            template_render_thread = None
```

### Mutant 264

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_264.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -671,7 +671,7 @@\n-                raise TemplateError(self._exc_info[1].with_traceback(self._exc_info[2]))\n+                raise TemplateError(self._exc_info[2].with_traceback(self._exc_info[2]))
```

### Mutant 265

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_265.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -671,7 +671,7 @@\n-                raise TemplateError(self._exc_info[1].with_traceback(self._exc_info[2]))\n+                raise TemplateError(self._exc_info[1].with_traceback(self._exc_info[3]))
```

### Mutant 266

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_266.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -674,7 +674,7 @@\n-            return True\n+            return False
```

### Mutant 267

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_267.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -678,7 +678,7 @@\n-        return False\n+        return True
```

### Mutant 268

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_268.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -680,7 +680,6 @@\n-    @callback
```

### Mutant 269

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_269.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -684,7 +684,7 @@\n-        strict: bool = False,\n+        strict: bool = True,
```

### Mutant 270

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_270.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -689,7 +689,7 @@\n-        if self.hass and self.hass.config.debug:\n+        if self.hass or self.hass.config.debug:
```

### Mutant 272

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_272.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -691,7 +691,7 @@\n-        self._renders += 1\n+        self._renders = 1
```

### Mutant 273

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_273.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -691,7 +691,7 @@\n-        self._renders += 1\n+        self._renders -= 1
```

### Mutant 274

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_274.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -691,7 +691,7 @@\n-        self._renders += 1\n+        self._renders += 2
```

### Mutant 275

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_275.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -693,7 +693,7 @@\n-        render_info = RenderInfo(self)\n+        render_info = None
```

### Mutant 276

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_276.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -695,7 +695,7 @@\n-        if not self.hass:\n+        if  self.hass:
```

### Mutant 278

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_278.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -698,7 +698,7 @@\n-        if _render_info.get() is not None:\n+        if _render_info.get() is  None:
```

### Mutant 282

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_282.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -706,7 +706,7 @@\n-            render_info._result = self.template.strip()  # noqa: SLF001\n+            render_info._result = None  # noqa: SLF001
```

### Mutant 283

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_283.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -710,7 +710,7 @@\n-        token = _render_info.set(render_info)\n+        token = None
```

### Mutant 284

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_284.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -712,9 +712,7 @@\n-            render_info._result = self.async_render(  # noqa: SLF001\n-                variables, strict=strict, log_fn=log_fn, **kwargs\n-            )\n+            render_info._result = None
```

### Mutant 285

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_285.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -716,7 +716,7 @@\n-            render_info.exception = ex\n+            render_info.exception = None
```

### Mutant 286

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_286.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -738,7 +738,6 @@\n-    @callback
```

### Mutant 288

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_288.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -752,7 +752,7 @@\n-        self._renders += 1\n+        self._renders = 1
```

### Mutant 289

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_289.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -752,7 +752,7 @@\n-        self._renders += 1\n+        self._renders -= 1
```

### Mutant 290

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_290.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -752,7 +752,7 @@\n-        self._renders += 1\n+        self._renders += 2
```

### Mutant 293

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_293.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -759,7 +759,7 @@\n-        variables = dict(variables or {})\n+        variables = dict(variables and {})
```

### Mutant 296

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_296.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -760,7 +760,7 @@\n-        variables["value"] = value\n+        variables["value"] = None
```

### Mutant 300

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_300.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -772,7 +772,7 @@\n-            if error_value is _SENTINEL:\n+            if error_value is not _SENTINEL:
```

### Mutant 302

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_302.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -779,7 +779,7 @@\n-            return value if error_value is _SENTINEL else error_value\n+            return value if error_value is not _SENTINEL else error_value
```

### Mutant 304

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_304.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -781,7 +781,7 @@\n-        if not parse_result or self.hass and self.hass.config.legacy_templates:\n+        if not parse_result or self.hass or self.hass.config.legacy_templates:
```

### Mutant 306

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_306.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -788,7 +788,7 @@\n-        limited: bool = False,\n+        limited: bool = True,
```

### Mutant 307

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_307.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -789,7 +789,7 @@\n-        strict: bool = False,\n+        strict: bool = True,
```

### Mutant 329

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_329.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -810,7 +810,7 @@\n-        self._log_fn = log_fn\n+        self._log_fn = None
```

### Mutant 337

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_337.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -835,8 +835,6 @@\n-\n-@cache
```

### Mutant 347

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_347.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -865,7 +865,7 @@\n-        if not valid_domain(name):\n+        if  valid_domain(name):
```

### Mutant 349

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_349.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -872,7 +872,7 @@\n-    __getitem__ = __getattr__\n+    __getitem__ = None
```

### Mutant 350

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_350.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -875,7 +875,7 @@\n-        if (render_info := _render_info.get()) is not None:\n+        if (render_info := _render_info.get()) is  None:
```

### Mutant 351

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_351.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -876,7 +876,7 @@\n-            render_info.all_states = True\n+            render_info.all_states = False
```

### Mutant 352

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_352.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -876,7 +876,7 @@\n-            render_info.all_states = True\n+            render_info.all_states = None
```

### Mutant 353

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_353.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -879,7 +879,7 @@\n-        if (render_info := _render_info.get()) is not None:\n+        if (render_info := _render_info.get()) is  None:
```

### Mutant 354

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_354.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -880,7 +880,7 @@\n-            render_info.all_states_lifecycle = True\n+            render_info.all_states_lifecycle = False
```

### Mutant 355

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_355.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -880,7 +880,7 @@\n-            render_info.all_states_lifecycle = True\n+            render_info.all_states_lifecycle = None
```

### Mutant 365

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_365.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -924,7 +924,7 @@\n-        if state is None:\n+        if state is not None:
```

### Mutant 366

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_366.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -927,7 +927,7 @@\n-        state_value = state.state\n+        state_value = None
```

### Mutant 367

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_367.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -928,7 +928,7 @@\n-        domain = state.domain\n+        domain = None
```

### Mutant 369

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_369.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -929,7 +929,7 @@\n-        device_class = state.attributes.get("device_class")\n+        device_class = None
```

### Mutant 370

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_370.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -930,7 +930,7 @@\n-        entry = entity_registry.async_get(self._hass).async_get(entity_id)\n+        entry = None
```

### Mutant 373

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_373.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -932,7 +932,7 @@\n-        translation_key = None if entry is None else entry.translation_key\n+        translation_key = None if entry is not None else entry.translation_key
```

### Mutant 374

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_374.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -932,7 +932,7 @@\n-        translation_key = None if entry is None else entry.translation_key\n+        translation_key = None
```

### Mutant 384

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_384.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -962,7 +962,7 @@\n-    __getitem__ = __getattr__\n+    __getitem__ = None
```

### Mutant 385

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_385.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -965,7 +965,7 @@\n-        if (entity_collect := _render_info.get()) is not None:\n+        if (entity_collect := _render_info.get()) is  None:
```

### Mutant 386

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_386.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -969,7 +969,7 @@\n-        if (entity_collect := _render_info.get()) is not None:\n+        if (entity_collect := _render_info.get()) is  None:
```

### Mutant 392

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_392.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1001,7 +1001,7 @@\n-        self._entity_id = entity_id\n+        self._entity_id = None
```

### Mutant 393

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_393.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1004,7 +1004,7 @@\n-        if self._collect and (render_info := _render_info.get()):\n+        if self._collect or (render_info := _render_info.get()):
```

### Mutant 394

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_394.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1011,7 +1011,7 @@\n-        if item in _COLLECTABLE_STATE_ATTRIBUTES:\n+        if item not in _COLLECTABLE_STATE_ATTRIBUTES:
```

### Mutant 395

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_395.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1013,7 +1013,7 @@\n-            if self._collect and (render_info := _render_info.get()):\n+            if self._collect or (render_info := _render_info.get()):
```

### Mutant 396

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_396.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1016,7 +1016,7 @@\n-        if item == "entity_id":\n+        if item != "entity_id":
```

### Mutant 432

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_432.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1154,7 +1154,7 @@\n-    if (entity_collect := _render_info.get()) is not None:\n+    if (entity_collect := _render_info.get()) is  None:
```

### Mutant 434

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_434.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1172,7 +1172,7 @@\n-    if domain is None:\n+    if domain is not None:
```

### Mutant 435

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_435.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1173,7 +1173,7 @@\n-        container = states._states.values()  # noqa: SLF001\n+        container = None  # noqa: SLF001
```

### Mutant 436

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_436.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1175,7 +1175,7 @@\n-        container = states.async_all(domain)\n+        container = None
```

### Mutant 437

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_437.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1181,7 +1181,7 @@\n-    state = hass.states.get(entity_id)\n+    state = None
```

### Mutant 438

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_438.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1182,7 +1182,7 @@\n-    if state is None and not valid_entity_id(entity_id):\n+    if state is not None and not valid_entity_id(entity_id):
```

### Mutant 439

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_439.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1182,7 +1182,7 @@\n-    if state is None and not valid_entity_id(entity_id):\n+    if state is None and  valid_entity_id(entity_id):
```

### Mutant 440

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_440.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1182,7 +1182,7 @@\n-    if state is None and not valid_entity_id(entity_id):\n+    if state is None or not valid_entity_id(entity_id):
```

### Mutant 443

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_443.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1212,8 +1212,6 @@\n-\n-@overload
```

### Mutant 444

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_444.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1216,8 +1216,6 @@\n-\n-@overload
```

### Mutant 445

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_445.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1231,7 +1231,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 447

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_447.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1243,7 +1243,7 @@\n-    if template_result is None:\n+    if template_result is not None:
```

### Mutant 448

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_448.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1244,7 +1244,7 @@\n-        return False\n+        return True
```

### Mutant 449

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_449.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1246,7 +1246,7 @@\n-    return forgiving_boolean(template_result, default=False)\n+    return forgiving_boolean(template_result, default=True)
```

### Mutant 478

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_478.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1287,7 +1287,7 @@\n-            found[entity_id] = entity\n+            found[entity_id] = None
```

### Mutant 497

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_497.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1364,7 +1364,7 @@\n-    device_reg = device_registry.async_get(hass)\n+    device_reg = None
```

### Mutant 498

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_498.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1365,7 +1365,7 @@\n-    if not isinstance(device_or_entity_id, str):\n+    if  isinstance(device_or_entity_id, str):
```

### Mutant 500

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_500.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1367,7 +1367,7 @@\n-    device = None\n+    device = ""
```

### Mutant 502

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_502.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1369,7 +1369,7 @@\n-        "." in device_or_entity_id\n+        "." not in device_or_entity_id
```

### Mutant 504

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_504.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1369,8 +1369,7 @@\n-        "." in device_or_entity_id\n-        and (_device_id := device_id(hass, device_or_entity_id)) is not None\n+        "." in device_or_entity_id or (_device_id := device_id(hass, device_or_entity_id)) is not None
```

### Mutant 512

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_512.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1384,7 +1384,7 @@\n-    return bool(device_attr(hass, device_or_entity_id, attr_name) == attr_value)\n+    return bool(device_attr(hass, device_or_entity_id, attr_name) != attr_value)
```

### Mutant 514

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_514.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1396,7 +1396,7 @@\n-    result = issue_registry.async_get(hass).async_get_issue(domain, issue_id)\n+    result = None
```

### Mutant 516

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_516.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1410,7 +1410,7 @@\n-    floor_registry = fr.async_get(hass)\n+    floor_registry = None
```

### Mutant 517

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_517.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1415,7 +1415,7 @@\n-        area_reg = area_registry.async_get(hass)\n+        area_reg = None
```

### Mutant 518

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_518.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1424,7 +1424,7 @@\n-    floor_registry = fr.async_get(hass)\n+    floor_registry = None
```

### Mutant 519

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_519.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1429,7 +1429,7 @@\n-        area_reg = area_registry.async_get(hass)\n+        area_reg = None
```

### Mutant 520

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_520.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1431,8 +1431,7 @@\n-            (area := area_reg.async_get_area(aid))\n-            and area.floor_id\n+            (area := area_reg.async_get_area(aid)) or area.floor_id
```

### Mutant 521

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_521.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1445,7 +1445,7 @@\n-    if floor_name(hass, floor_id_or_name) is not None:\n+    if floor_name(hass, floor_id_or_name) is  None:
```

### Mutant 522

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_522.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1446,7 +1446,7 @@\n-        _floor_id = floor_id_or_name\n+        _floor_id = None
```

### Mutant 527

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_527.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1464,7 +1464,7 @@\n-    area_reg = area_registry.async_get(hass)\n+    area_reg = None
```

### Mutant 528

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_528.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1468,7 +1468,7 @@\n-    ent_reg = entity_registry.async_get(hass)\n+    ent_reg = None
```

### Mutant 532

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_532.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1502,7 +1502,7 @@\n-    area_reg = area_registry.async_get(hass)\n+    area_reg = None
```

### Mutant 533

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_533.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1506,7 +1506,7 @@\n-    dev_reg = device_registry.async_get(hass)\n+    dev_reg = None
```

### Mutant 536

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_536.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1529,7 +1529,7 @@\n-    if (device := dev_reg.async_get(lookup_value)) and device.area_id:\n+    if (device := dev_reg.async_get(lookup_value)) or device.area_id:
```

### Mutant 537

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_537.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1540,7 +1540,7 @@\n-    if area_name(hass, area_id_or_name) is None:\n+    if area_name(hass, area_id_or_name) is not None:
```

### Mutant 538

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_538.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1541,7 +1541,7 @@\n-        _area_id = area_id(hass, area_id_or_name)\n+        _area_id = None
```

### Mutant 545

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_545.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1570,7 +1570,7 @@\n-    if area_name(hass, area_id_or_name) is not None:\n+    if area_name(hass, area_id_or_name) is  None:
```

### Mutant 546

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_546.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1571,7 +1571,7 @@\n-        _area_id = area_id_or_name\n+        _area_id = None
```

### Mutant 551

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_551.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1583,7 +1583,7 @@\n-    label_reg = label_registry.async_get(hass)\n+    label_reg = None
```

### Mutant 552

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_552.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1584,7 +1584,7 @@\n-    if lookup_value is None:\n+    if lookup_value is not None:
```

### Mutant 553

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_553.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1587,7 +1587,7 @@\n-    ent_reg = entity_registry.async_get(hass)\n+    ent_reg = None
```

### Mutant 554

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_554.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1592,7 +1592,7 @@\n-    lookup_value = str(lookup_value)\n+    lookup_value = None
```

### Mutant 555

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_555.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1603,7 +1603,7 @@\n-    dev_reg = device_registry.async_get(hass)\n+    dev_reg = None
```

### Mutant 556

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_556.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1608,7 +1608,7 @@\n-    area_reg = area_registry.async_get(hass)\n+    area_reg = None
```

### Mutant 557

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_557.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1617,7 +1617,7 @@\n-    label_reg = label_registry.async_get(hass)\n+    label_reg = None
```

### Mutant 558

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_558.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1625,7 +1625,7 @@\n-    label_reg = label_registry.async_get(hass)\n+    label_reg = None
```

### Mutant 559

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_559.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1635,7 +1635,7 @@\n-    if label_name(hass, label_id_or_name) is not None:\n+    if label_name(hass, label_id_or_name) is  None:
```

### Mutant 605

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_605.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1745,7 +1745,7 @@\n-    to_process = list(args)\n+    to_process = None
```

### Mutant 606

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_606.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1748,7 +1748,7 @@\n-        value = to_process.pop(0)\n+        value = to_process.pop(1)
```

### Mutant 607

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_607.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1748,7 +1748,7 @@\n-        value = to_process.pop(0)\n+        value = None
```

### Mutant 608

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_608.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1749,7 +1749,7 @@\n-        if isinstance(value, str) and not valid_entity_id(value):\n+        if isinstance(value, str) and  valid_entity_id(value):
```

### Mutant 609

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_609.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1749,7 +1749,7 @@\n-        if isinstance(value, str) and not valid_entity_id(value):\n+        if isinstance(value, str) or not valid_entity_id(value):
```

### Mutant 610

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_610.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1750,7 +1750,7 @@\n-            point_state = None\n+            point_state = ""
```

### Mutant 611

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_611.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1752,7 +1752,7 @@\n-            point_state = _resolve_state(hass, value)\n+            point_state = None
```

### Mutant 612

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_612.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1754,7 +1754,7 @@\n-        if point_state is None:\n+        if point_state is not None:
```

### Mutant 613

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_613.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1756,7 +1756,7 @@\n-            if not to_process:\n+            if  to_process:
```

### Mutant 615

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_615.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1762,7 +1762,7 @@\n-            value_2 = to_process.pop(0)\n+            value_2 = to_process.pop(1)
```

### Mutant 616

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_616.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1762,7 +1762,7 @@\n-            value_2 = to_process.pop(0)\n+            value_2 = None
```

### Mutant 617

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_617.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1763,7 +1763,7 @@\n-            latitude = convert(value, float)\n+            latitude = None
```

### Mutant 618

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_618.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1764,7 +1764,7 @@\n-            longitude = convert(value_2, float)\n+            longitude = None
```

### Mutant 619

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_619.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1766,7 +1766,7 @@\n-            if latitude is None or longitude is None:\n+            if latitude is not None or longitude is None:
```

### Mutant 620

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_620.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1766,7 +1766,7 @@\n-            if latitude is None or longitude is None:\n+            if latitude is None or longitude is not None:
```

### Mutant 621

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_621.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1766,7 +1766,7 @@\n-            if latitude is None or longitude is None:\n+            if latitude is None and longitude is None:
```

### Mutant 637

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_637.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1803,7 +1803,7 @@\n-    state_obj = _get_state(hass, entity_id)\n+    state_obj = None
```

### Mutant 638

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_638.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1804,7 +1804,7 @@\n-    return state_obj is not None and (\n+    return state_obj is  None and (
```

### Mutant 639

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_639.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1805,7 +1805,7 @@\n-        state_obj.state == state or isinstance(state, list) and state_obj.state in state\n+        state_obj.state != state or isinstance(state, list) and state_obj.state in state
```

### Mutant 640

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_640.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1805,7 +1805,7 @@\n-        state_obj.state == state or isinstance(state, list) and state_obj.state in state\n+        state_obj.state == state or isinstance(state, list) and state_obj.state not in state
```

### Mutant 641

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_641.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1805,7 +1805,7 @@\n-        state_obj.state == state or isinstance(state, list) and state_obj.state in state\n+        state_obj.state == state or isinstance(state, list) or state_obj.state in state
```

### Mutant 642

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_642.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1805,7 +1805,7 @@\n-        state_obj.state == state or isinstance(state, list) and state_obj.state in state\n+        state_obj.state == state and isinstance(state, list) and state_obj.state in state
```

### Mutant 643

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_643.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1804,7 +1804,7 @@\n-    return state_obj is not None and (\n+    return state_obj is not None or (
```

### Mutant 644

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_644.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1811,7 +1811,7 @@\n-    attr = state_attr(hass, entity_id, name)\n+    attr = None
```

### Mutant 645

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_645.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1812,7 +1812,7 @@\n-    return attr is not None and attr == value\n+    return attr is  None and attr == value
```

### Mutant 646

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_646.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1812,7 +1812,7 @@\n-    return attr is not None and attr == value\n+    return attr is not None and attr != value
```

### Mutant 647

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_647.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1812,7 +1812,7 @@\n-    return attr is not None and attr == value\n+    return attr is not None or attr == value
```

### Mutant 649

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_649.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1824,7 +1824,7 @@\n-    state_obj = _get_state(hass, entity_id)\n+    state_obj = None
```

### Mutant 650

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_650.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1826,7 +1826,7 @@\n-    return state_obj is not None and (\n+    return state_obj is  None and (
```

### Mutant 652

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_652.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1826,7 +1826,7 @@\n-    return state_obj is not None and (\n+    return state_obj is not None or (
```

### Mutant 653

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_653.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1833,7 +1833,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 654

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_654.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1834,7 +1834,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 655

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_655.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1834,7 +1834,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 656

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_656.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1841,7 +1841,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 657

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_657.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1842,7 +1842,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 658

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_658.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1842,7 +1842,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 661

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_661.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1849,7 +1849,7 @@\n-    template, action = template_cv.get() or ("", "rendering or compiling")\n+    template, action = template_cv.get() and ("", "rendering or compiling")
```

### Mutant 662

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_662.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1849,7 +1849,7 @@\n-    template, action = template_cv.get() or ("", "rendering or compiling")\n+    template, action = None
```

### Mutant 665

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_665.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1856,7 +1856,7 @@\n-def forgiving_round(value, precision=0, method="common", default=_SENTINEL):\n+def forgiving_round(value, precision=1, method="common", default=_SENTINEL):
```

### Mutant 667

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_667.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1860,7 +1860,7 @@\n-        multiplier = float(10**precision)\n+        multiplier = float(11**precision)
```

### Mutant 668

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_668.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1860,7 +1860,7 @@\n-        multiplier = float(10**precision)\n+        multiplier = float(10*precision)
```

### Mutant 669

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_669.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1860,7 +1860,7 @@\n-        multiplier = float(10**precision)\n+        multiplier = None
```

### Mutant 670

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_670.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1861,7 +1861,7 @@\n-        if method == "ceil":\n+        if method != "ceil":
```

### Mutant 672

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_672.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1862,7 +1862,7 @@\n-            value = math.ceil(float(value) * multiplier) / multiplier\n+            value = math.ceil(float(value) / multiplier) / multiplier
```

### Mutant 673

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_673.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1862,7 +1862,7 @@\n-            value = math.ceil(float(value) * multiplier) / multiplier\n+            value = math.ceil(float(value) * multiplier) * multiplier
```

### Mutant 674

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_674.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1862,7 +1862,7 @@\n-            value = math.ceil(float(value) * multiplier) / multiplier\n+            value = None
```

### Mutant 675

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_675.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1863,7 +1863,7 @@\n-        elif method == "floor":\n+        elif method != "floor":
```

### Mutant 677

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_677.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1864,7 +1864,7 @@\n-            value = math.floor(float(value) * multiplier) / multiplier\n+            value = math.floor(float(value) / multiplier) / multiplier
```

### Mutant 678

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_678.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1864,7 +1864,7 @@\n-            value = math.floor(float(value) * multiplier) / multiplier\n+            value = math.floor(float(value) * multiplier) * multiplier
```

### Mutant 679

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_679.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1864,7 +1864,7 @@\n-            value = math.floor(float(value) * multiplier) / multiplier\n+            value = None
```

### Mutant 680

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_680.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1865,7 +1865,7 @@\n-        elif method == "half":\n+        elif method != "half":
```

### Mutant 682

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_682.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1866,7 +1866,7 @@\n-            value = round(float(value) * 2) / 2\n+            value = round(float(value) / 2) / 2
```

### Mutant 683

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_683.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1866,7 +1866,7 @@\n-            value = round(float(value) * 2) / 2\n+            value = round(float(value) * 3) / 2
```

### Mutant 684

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_684.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1866,7 +1866,7 @@\n-            value = round(float(value) * 2) / 2\n+            value = round(float(value) * 2) * 2
```

### Mutant 685

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_685.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1866,7 +1866,7 @@\n-            value = round(float(value) * 2) / 2\n+            value = round(float(value) * 2) / 3
```

### Mutant 686

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_686.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1866,7 +1866,7 @@\n-            value = round(float(value) * 2) / 2\n+            value = None
```

### Mutant 687

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_687.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1869,7 +1869,7 @@\n-            value = round(float(value), precision)\n+            value = None
```

### Mutant 688

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_688.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1870,7 +1870,7 @@\n-        return int(value) if precision == 0 else value\n+        return int(value) if precision != 0 else value
```

### Mutant 689

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_689.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1870,7 +1870,7 @@\n-        return int(value) if precision == 0 else value\n+        return int(value) if precision == 1 else value
```

### Mutant 690

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_690.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1873,7 +1873,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 692

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_692.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1881,7 +1881,7 @@\n-        return float(value) * amount\n+        return float(value) / amount
```

### Mutant 693

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_693.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1884,7 +1884,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 695

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_695.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1892,7 +1892,7 @@\n-        return float(value) + amount\n+        return float(value) - amount
```

### Mutant 696

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_696.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1895,7 +1895,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 698

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_698.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1903,7 +1903,7 @@\n-        base_float = float(base)\n+        base_float = None
```

### Mutant 699

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_699.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1905,7 +1905,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 701

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_701.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1909,7 +1909,7 @@\n-        value_float = float(value)\n+        value_float = None
```

### Mutant 702

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_702.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1912,7 +1912,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 704

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_704.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1922,7 +1922,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 706

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_706.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1932,7 +1932,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 708

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_708.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1942,7 +1942,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 710

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_710.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1952,7 +1952,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 712

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_712.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1962,7 +1962,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 714

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_714.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1972,7 +1972,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 716

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_716.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 2 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):
```

### Mutant 717

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_717.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 1 < len(args) <= 2 and isinstance(args[0], (list, tuple)):
```

### Mutant 718

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_718.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 1 <= len(args) < 2 and isinstance(args[0], (list, tuple)):
```

### Mutant 719

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_719.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 1 <= len(args) <= 3 and isinstance(args[0], (list, tuple)):
```

### Mutant 720

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_720.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 1 <= len(args) <= 2 and isinstance(args[1], (list, tuple)):
```

### Mutant 721

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_721.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1984,7 +1984,7 @@\n-        if 1 <= len(args) <= 2 and isinstance(args[0], (list, tuple)):\n+        if 1 <= len(args) <= 2 or isinstance(args[0], (list, tuple)):
```

### Mutant 722

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_722.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1985,7 +1985,7 @@\n-            if len(args) == 2 and default is _SENTINEL:\n+            if len(args) != 2 and default is _SENTINEL:
```

### Mutant 723

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_723.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1985,7 +1985,7 @@\n-            if len(args) == 2 and default is _SENTINEL:\n+            if len(args) == 3 and default is _SENTINEL:
```

### Mutant 724

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_724.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1985,7 +1985,7 @@\n-            if len(args) == 2 and default is _SENTINEL:\n+            if len(args) == 2 and default is not _SENTINEL:
```

### Mutant 725

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_725.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1985,7 +1985,7 @@\n-            if len(args) == 2 and default is _SENTINEL:\n+            if len(args) == 2 or default is _SENTINEL:
```

### Mutant 726

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_726.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1987,7 +1987,7 @@\n-                default = args[1]\n+                default = args[2]
```

### Mutant 727

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_727.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1987,7 +1987,7 @@\n-                default = args[1]\n+                default = None
```

### Mutant 728

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_728.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1988,7 +1988,7 @@\n-            args = args[0]\n+            args = args[1]
```

### Mutant 729

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_729.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1988,7 +1988,7 @@\n-            args = args[0]\n+            args = None
```

### Mutant 730

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_730.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1989,7 +1989,7 @@\n-        elif len(args) == 3 and default is _SENTINEL:\n+        elif len(args) != 3 and default is _SENTINEL:
```

### Mutant 731

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_731.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1989,7 +1989,7 @@\n-        elif len(args) == 3 and default is _SENTINEL:\n+        elif len(args) == 4 and default is _SENTINEL:
```

### Mutant 732

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_732.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1989,7 +1989,7 @@\n-        elif len(args) == 3 and default is _SENTINEL:\n+        elif len(args) == 3 and default is not _SENTINEL:
```

### Mutant 733

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_733.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1989,7 +1989,7 @@\n-        elif len(args) == 3 and default is _SENTINEL:\n+        elif len(args) == 3 or default is _SENTINEL:
```

### Mutant 734

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_734.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1991,7 +1991,7 @@\n-            default = args[2]\n+            default = args[3]
```

### Mutant 735

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_735.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1991,7 +1991,7 @@\n-            default = args[2]\n+            default = None
```

### Mutant 736

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_736.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1993,7 +1993,7 @@\n-        return math.atan2(float(args[0]), float(args[1]))\n+        return math.atan2(float(args[1]), float(args[1]))
```

### Mutant 737

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_737.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1993,7 +1993,7 @@\n-        return math.atan2(float(args[0]), float(args[1]))\n+        return math.atan2(float(args[0]), float(args[2]))
```

### Mutant 738

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_738.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -1995,7 +1995,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 740

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_740.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2010,7 +2010,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 742

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_742.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2015,7 +2015,7 @@\n-def timestamp_custom(value, date_format=DATE_STR_FORMAT, local=True, default=_SENTINEL):\n+def timestamp_custom(value, date_format=DATE_STR_FORMAT, local=False, default=_SENTINEL):
```

### Mutant 743

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_743.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2018,7 +2018,7 @@\n-        result = dt_util.utc_from_timestamp(value)\n+        result = None
```

### Mutant 744

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_744.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2021,7 +2021,7 @@\n-            result = dt_util.as_local(result)\n+            result = None
```

### Mutant 745

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_745.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2026,7 +2026,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 747

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_747.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2037,7 +2037,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 749

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_749.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2048,7 +2048,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 751

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_751.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2058,7 +2058,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 753

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_753.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2066,7 +2066,7 @@\n-    if type(value) is datetime:\n+    if type(value) is not datetime:
```

### Mutant 754

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_754.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2069,7 +2069,7 @@\n-    if type(value) is date:\n+    if type(value) is not date:
```

### Mutant 755

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_755.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2070,7 +2070,7 @@\n-        return datetime.combine(value, time(0, 0, 0))\n+        return datetime.combine(value, time(1, 0, 0))
```

### Mutant 756

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_756.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2070,7 +2070,7 @@\n-        return datetime.combine(value, time(0, 0, 0))\n+        return datetime.combine(value, time(0, 1, 0))
```

### Mutant 757

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_757.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2070,7 +2070,7 @@\n-        return datetime.combine(value, time(0, 0, 0))\n+        return datetime.combine(value, time(0, 0, 1))
```

### Mutant 758

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_758.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2073,7 +2073,7 @@\n-        timestamp = float(value)\n+        timestamp = None
```

### Mutant 759

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_759.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2078,7 +2078,7 @@\n-            return dt_util.parse_datetime(value, raise_on_error=True)\n+            return dt_util.parse_datetime(value, raise_on_error=False)
```

### Mutant 760

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_760.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2080,7 +2080,7 @@\n-            if default is _SENTINEL:\n+            if default is not _SENTINEL:
```

### Mutant 762

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_762.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2099,7 +2099,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 764

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_764.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2117,7 +2117,6 @@\n-    @pass_environment
```

### Mutant 765

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_765.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2118,7 +2118,7 @@\n-    @wraps(builtin_filter)\n+
```

### Mutant 766

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_766.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2120,7 +2120,7 @@\n-        if len(args) == 0:\n+        if len(args) != 0:
```

### Mutant 767

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_767.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2120,7 +2120,7 @@\n-        if len(args) == 0:\n+        if len(args) == 1:
```

### Mutant 838

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_838.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2228,7 +2228,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 840

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_840.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2238,7 +2238,7 @@\n-        if default is _SENTINEL:\n+        if default is not _SENTINEL:
```

### Mutant 842

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_842.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2243,7 +2243,7 @@\n-def forgiving_int(value, default=_SENTINEL, base=10):\n+def forgiving_int(value, default=_SENTINEL, base=11):
```

### Mutant 843

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_843.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2245,7 +2245,7 @@\n-    result = jinja2.filters.do_int(value, default=default, base=base)\n+    result = None
```

### Mutant 844

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_844.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2246,7 +2246,7 @@\n-    if result is _SENTINEL:\n+    if result is not _SENTINEL:
```

### Mutant 846

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_846.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2251,7 +2251,7 @@\n-def forgiving_int_filter(value, default=_SENTINEL, base=10):\n+def forgiving_int_filter(value, default=_SENTINEL, base=11):
```

### Mutant 847

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_847.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2253,7 +2253,7 @@\n-    result = jinja2.filters.do_int(value, default=default, base=base)\n+    result = None
```

### Mutant 848

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_848.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2254,7 +2254,7 @@\n-    if result is _SENTINEL:\n+    if result is not _SENTINEL:
```

### Mutant 850

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_850.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2262,7 +2262,7 @@\n-        fvalue = float(value)\n+        fvalue = None
```

### Mutant 851

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_851.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2264,7 +2264,7 @@\n-        return False\n+        return True
```

### Mutant 852

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_852.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2265,7 +2265,7 @@\n-    if not math.isfinite(fvalue):\n+    if  math.isfinite(fvalue):
```

### Mutant 853

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_853.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2266,7 +2266,7 @@\n-        return False\n+        return True
```

### Mutant 854

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_854.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2267,7 +2267,7 @@\n-    return True\n+    return False
```

### Mutant 856

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_856.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2305,7 +2305,7 @@\n-def regex_match(value, find="", ignorecase=False):\n+def regex_match(value, find="", ignorecase=True):
```

### Mutant 857

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_857.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2307,7 +2307,7 @@\n-    if not isinstance(value, str):\n+    if  isinstance(value, str):
```

### Mutant 858

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_858.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2308,7 +2308,7 @@\n-        value = str(value)\n+        value = None
```

### Mutant 859

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_859.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2309,7 +2309,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = re.I if ignorecase else 1
```

### Mutant 860

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_860.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2309,7 +2309,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = None
```

### Mutant 861

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_861.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2313,7 +2313,7 @@\n-_regex_cache = lru_cache(maxsize=128)(re.compile)\n+_regex_cache = lru_cache(maxsize=129)(re.compile)
```

### Mutant 862

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_862.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2313,7 +2313,7 @@\n-_regex_cache = lru_cache(maxsize=128)(re.compile)\n+_regex_cache = None
```

### Mutant 866

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_866.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2316,7 +2316,7 @@\n-def regex_replace(value="", find="", replace="", ignorecase=False):\n+def regex_replace(value="", find="", replace="", ignorecase=True):
```

### Mutant 867

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_867.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2318,7 +2318,7 @@\n-    if not isinstance(value, str):\n+    if  isinstance(value, str):
```

### Mutant 868

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_868.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2319,7 +2319,7 @@\n-        value = str(value)\n+        value = None
```

### Mutant 869

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_869.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2320,7 +2320,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = re.I if ignorecase else 1
```

### Mutant 870

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_870.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2320,7 +2320,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = None
```

### Mutant 872

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_872.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2324,7 +2324,7 @@\n-def regex_search(value, find="", ignorecase=False):\n+def regex_search(value, find="", ignorecase=True):
```

### Mutant 873

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_873.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2326,7 +2326,7 @@\n-    if not isinstance(value, str):\n+    if  isinstance(value, str):
```

### Mutant 874

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_874.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2327,7 +2327,7 @@\n-        value = str(value)\n+        value = None
```

### Mutant 875

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_875.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2328,7 +2328,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = re.I if ignorecase else 1
```

### Mutant 876

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_876.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2328,7 +2328,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = None
```

### Mutant 878

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_878.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2332,7 +2332,7 @@\n-def regex_findall_index(value, find="", index=0, ignorecase=False):\n+def regex_findall_index(value, find="", index=1, ignorecase=False):
```

### Mutant 879

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_879.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2332,7 +2332,7 @@\n-def regex_findall_index(value, find="", index=0, ignorecase=False):\n+def regex_findall_index(value, find="", index=0, ignorecase=True):
```

### Mutant 881

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_881.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2337,7 +2337,7 @@\n-def regex_findall(value, find="", ignorecase=False):\n+def regex_findall(value, find="", ignorecase=True):
```

### Mutant 882

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_882.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2339,7 +2339,7 @@\n-    if not isinstance(value, str):\n+    if  isinstance(value, str):
```

### Mutant 883

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_883.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2340,7 +2340,7 @@\n-        value = str(value)\n+        value = None
```

### Mutant 884

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_884.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2341,7 +2341,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = re.I if ignorecase else 1
```

### Mutant 885

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_885.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2341,7 +2341,7 @@\n-    flags = re.I if ignorecase else 0\n+    flags = None
```

### Mutant 886

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_886.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2347,7 +2347,7 @@\n-    return first_value & second_value\n+    return first_value | second_value
```

### Mutant 887

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_887.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2352,7 +2352,7 @@\n-    return first_value | second_value\n+    return first_value & second_value
```

### Mutant 888

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_888.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2357,7 +2357,7 @@\n-    return first_value ^ second_value\n+    return first_value & second_value
```

### Mutant 892

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_892.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2378,7 +2378,7 @@\n-def struct_unpack(value: bytes, format_string: str, offset: int = 0) -> Any | None:\n+def struct_unpack(value: bytes, format_string: str, offset: int = 1) -> Any | None:
```

### Mutant 893

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_893.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2381,7 +2381,7 @@\n-        return unpack_from(format_string, value, offset)[0]\n+        return unpack_from(format_string, value, offset)[1]
```

### Mutant 904

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_904.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2408,7 +2408,7 @@\n-    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6  # codespell:ignore nd\n+    suffixes = ["th", "st", "nd", "rd"] - ["th"] * 6  # codespell:ignore nd
```

### Mutant 906

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_906.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2408,7 +2408,7 @@\n-    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6  # codespell:ignore nd\n+    suffixes = ["th", "st", "nd", "rd"] + ["th"] / 6  # codespell:ignore nd
```

### Mutant 907

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_907.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2408,7 +2408,7 @@\n-    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6  # codespell:ignore nd\n+    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 7  # codespell:ignore nd
```

### Mutant 908

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_908.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2408,7 +2408,7 @@\n-    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6  # codespell:ignore nd\n+    suffixes = None  # codespell:ignore nd
```

### Mutant 909

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_909.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2409,7 +2409,7 @@\n-    return str(value) + (\n+    return str(value) - (
```

### Mutant 910

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_910.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2410,7 +2410,7 @@\n-        suffixes[(int(str(value)[-1])) % 10]\n+        suffixes[(int(str(value)[+1])) % 10]
```

### Mutant 911

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_911.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2410,7 +2410,7 @@\n-        suffixes[(int(str(value)[-1])) % 10]\n+        suffixes[(int(str(value)[-2])) % 10]
```

### Mutant 912

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_912.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2410,7 +2410,7 @@\n-        suffixes[(int(str(value)[-1])) % 10]\n+        suffixes[(int(str(value)[-1])) / 10]
```

### Mutant 913

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_913.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2410,7 +2410,7 @@\n-        suffixes[(int(str(value)[-1])) % 10]\n+        suffixes[(int(str(value)[-1])) % 11]
```

### Mutant 914

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_914.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[+2:]) % 100 not in range(11, 14)
```

### Mutant 915

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_915.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-3:]) % 100 not in range(11, 14)
```

### Mutant 916

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_916.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-2:]) / 100 not in range(11, 14)
```

### Mutant 917

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_917.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-2:]) % 101 not in range(11, 14)
```

### Mutant 918

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_918.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-2:]) % 100  in range(11, 14)
```

### Mutant 919

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_919.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-2:]) % 100 not in range(12, 14)
```

### Mutant 920

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_920.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2411,7 +2411,7 @@\n-        if int(str(value)[-2:]) % 100 not in range(11, 14)\n+        if int(str(value)[-2:]) % 100 not in range(11, 15)
```

### Mutant 923

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_923.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2428,7 +2428,7 @@\n-    ensure_ascii: bool = False,\n+    ensure_ascii: bool = True,
```

### Mutant 924

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_924.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2429,7 +2429,7 @@\n-    pretty_print: bool = False,\n+    pretty_print: bool = True,
```

### Mutant 925

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_925.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2430,7 +2430,7 @@\n-    sort_keys: bool = False,\n+    sort_keys: bool = True,
```

### Mutant 926

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_926.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2438,7 +2438,7 @@\n-            indent=2 if pretty_print else None,\n+            indent=3 if pretty_print else None,
```

### Mutant 932

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_932.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2442,15 +2442,7 @@\n-    option = (\n-        ORJSON_PASSTHROUGH_OPTIONS\n-        # OPT_NON_STR_KEYS is added as a workaround to\n-        # ensure subclasses of str are allowed as dict keys\n-        # See: https://github.com/ijl/orjson/issues/445\n-        | orjson.OPT_NON_STR_KEYS\n-        | (orjson.OPT_INDENT_2 if pretty_print else 0)
```

### Mutant 934

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_934.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2458,8 +2458,6 @@\n-\n-@pass_context
```

### Mutant 936

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_936.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2471,7 +2471,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 937

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_937.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2472,7 +2472,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 938

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_938.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2472,7 +2472,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 939

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_939.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2474,7 +2474,7 @@\n-    today = dt_util.start_of_local_day()\n+    today = None
```

### Mutant 941

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_941.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2478,7 +2478,7 @@\n-    if (time_today := dt_util.parse_time(time_str)) is None:\n+    if (time_today := dt_util.parse_time(time_str)) is not None:
```

### Mutant 943

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_943.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2501,7 +2501,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 944

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_944.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2502,7 +2502,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 945

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_945.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2502,7 +2502,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 946

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_946.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2504,7 +2504,7 @@\n-    if not isinstance(value, datetime):\n+    if  isinstance(value, datetime):
```

### Mutant 947

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_947.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2506,7 +2506,7 @@\n-    if not value.tzinfo:\n+    if  value.tzinfo:
```

### Mutant 948

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_948.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2507,7 +2507,7 @@\n-        value = dt_util.as_local(value)\n+        value = None
```

### Mutant 949

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_949.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2508,7 +2508,7 @@\n-    if dt_util.now() < value:\n+    if dt_util.now() <= value:
```

### Mutant 950

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_950.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2513,7 +2513,7 @@\n-def time_since(hass: HomeAssistant, value: Any | datetime, precision: int = 1) -> Any:\n+def time_since(hass: HomeAssistant, value: Any | datetime, precision: int = 2) -> Any:
```

### Mutant 951

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_951.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2522,7 +2522,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 952

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_952.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2523,7 +2523,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 953

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_953.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2523,7 +2523,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 954

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_954.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2525,7 +2525,7 @@\n-    if not isinstance(value, datetime):\n+    if  isinstance(value, datetime):
```

### Mutant 955

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_955.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2527,7 +2527,7 @@\n-    if not value.tzinfo:\n+    if  value.tzinfo:
```

### Mutant 956

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_956.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2528,7 +2528,7 @@\n-        value = dt_util.as_local(value)\n+        value = None
```

### Mutant 957

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_957.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2529,7 +2529,7 @@\n-    if dt_util.now() < value:\n+    if dt_util.now() <= value:
```

### Mutant 958

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_958.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2535,7 +2535,7 @@\n-def time_until(hass: HomeAssistant, value: Any | datetime, precision: int = 1) -> Any:\n+def time_until(hass: HomeAssistant, value: Any | datetime, precision: int = 2) -> Any:
```

### Mutant 959

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_959.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2544,7 +2544,7 @@\n-    if (render_info := _render_info.get()) is not None:\n+    if (render_info := _render_info.get()) is  None:
```

### Mutant 960

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_960.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2545,7 +2545,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = False
```

### Mutant 961

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_961.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2545,7 +2545,7 @@\n-        render_info.has_time = True\n+        render_info.has_time = None
```

### Mutant 962

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_962.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2547,7 +2547,7 @@\n-    if not isinstance(value, datetime):\n+    if  isinstance(value, datetime):
```

### Mutant 963

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_963.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2549,7 +2549,7 @@\n-    if not value.tzinfo:\n+    if  value.tzinfo:
```

### Mutant 964

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_964.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2550,7 +2550,7 @@\n-        value = dt_util.as_local(value)\n+        value = None
```

### Mutant 965

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_965.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2551,7 +2551,7 @@\n-    if dt_util.now() > value:\n+    if dt_util.now() >= value:
```

### Mutant 968

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_968.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2568,7 +2568,7 @@\n-    value: Any, if_true: Any = True, if_false: Any = False, if_none: Any = _SENTINEL\n+    value: Any, if_true: Any = False, if_false: Any = False, if_none: Any = _SENTINEL
```

### Mutant 969

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_969.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2568,7 +2568,7 @@\n-    value: Any, if_true: Any = True, if_false: Any = False, if_none: Any = _SENTINEL\n+    value: Any, if_true: Any = True, if_false: Any = True, if_none: Any = _SENTINEL
```

### Mutant 970

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_970.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2580,7 +2580,7 @@\n-    if value is None and if_none is not _SENTINEL:\n+    if value is not None and if_none is not _SENTINEL:
```

### Mutant 971

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_971.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2580,7 +2580,7 @@\n-    if value is None and if_none is not _SENTINEL:\n+    if value is None and if_none is  _SENTINEL:
```

### Mutant 972

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_972.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2580,7 +2580,7 @@\n-    if value is None and if_none is not _SENTINEL:\n+    if value is None or if_none is not _SENTINEL:
```

### Mutant 977

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_977.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2625,7 +2625,7 @@\n-        template, action = template_cv.get() or ("", "rendering or compiling")\n+        template, action = template_cv.get() and ("", "rendering or compiling")
```

### Mutant 978

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_978.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2625,7 +2625,7 @@\n-        template, action = template_cv.get() or ("", "rendering or compiling")\n+        template, action = None
```

### Mutant 980

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_980.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2635,7 +2635,7 @@\n-    _log_fn = log_fn or _log_with_logger\n+    _log_fn = log_fn and _log_with_logger
```

### Mutant 981

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_981.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2635,7 +2635,7 @@\n-    _log_fn = log_fn or _log_with_logger\n+    _log_fn = None
```

### Mutant 982

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_982.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2670,7 +2670,7 @@\n-    custom_templates = await hass.async_add_executor_job(_load_custom_templates, hass)\n+    custom_templates = None
```

### Mutant 983

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_983.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2671,7 +2671,7 @@\n-    _get_hass_loader(hass).sources = custom_templates\n+    _get_hass_loader(hass).sources = None
```

### Mutant 984

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_984.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2675,7 +2675,7 @@\n-    result = {}\n+    result = None
```

### Mutant 988

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_988.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2680,7 +2680,7 @@\n-        if item.is_file() and item.stat().st_size <= MAX_CUSTOM_TEMPLATE_SIZE\n+        if item.is_file() and item.stat().st_size < MAX_CUSTOM_TEMPLATE_SIZE
```

### Mutant 989

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_989.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2680,7 +2680,7 @@\n-        if item.is_file() and item.stat().st_size <= MAX_CUSTOM_TEMPLATE_SIZE\n+        if item.is_file() or item.stat().st_size <= MAX_CUSTOM_TEMPLATE_SIZE
```

### Mutant 991

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_991.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2683,7 +2683,7 @@\n-        content = file.read_text()\n+        content = None
```

### Mutant 992

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_992.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2684,7 +2684,7 @@\n-        path = str(file.relative_to(jinja_path))\n+        path = None
```

### Mutant 993

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_993.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2685,7 +2685,7 @@\n-        result[path] = content\n+        result[path] = None
```

### Mutant 994

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_994.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2688,8 +2688,6 @@\n-\n-@singleton(_HASS_LOADER)
```

### Mutant 999

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_999.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2707,7 +2707,6 @@\n-    @sources.setter
```

### Mutant 1000

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1000.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2709,7 +2709,7 @@\n-        self._sources = value\n+        self._sources = None
```

### Mutant 1001

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1001.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2710,7 +2710,7 @@\n-        self._reload += 1\n+        self._reload = 1
```

### Mutant 1002

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1002.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2710,7 +2710,7 @@\n-        self._reload += 1\n+        self._reload -= 1
```

### Mutant 1003

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1003.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2710,7 +2710,7 @@\n-        self._reload += 1\n+        self._reload += 2
```

### Mutant 1004

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1004.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2716,7 +2716,7 @@\n-        if template not in self._sources:\n+        if template  in self._sources:
```

### Mutant 1005

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1005.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2718,7 +2718,7 @@\n-        cur_reload = self._reload\n+        cur_reload = None
```

### Mutant 1006

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1006.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2719,7 +2719,7 @@\n-        return self._sources[template], template, lambda: cur_reload == self._reload\n+        return self._sources[template], template, lambda: cur_reload != self._reload
```

### Mutant 1007

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1007.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2719,7 +2719,7 @@\n-        return self._sources[template], template, lambda: cur_reload == self._reload\n+        return self._sources[template], template, lambda: None
```

### Mutant 1010

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1010.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2734,7 +2734,7 @@\n-        self.hass = hass\n+        self.hass = None
```

### Mutant 1011

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1011.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2736,7 +2736,7 @@\n-            str | jinja2.nodes.Template, CodeType | None\n+            str & jinja2.nodes.Template, CodeType | None
```

### Mutant 1012

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1012.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2736,7 +2736,7 @@\n-            str | jinja2.nodes.Template, CodeType | None\n+            str | jinja2.nodes.Template, CodeType & None
```

### Mutant 1016

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1016.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2739,7 +2739,7 @@\n-        self.filters["round"] = forgiving_round\n+        self.filters["round"] = None
```

### Mutant 1018

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1018.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2740,7 +2740,7 @@\n-        self.filters["multiply"] = multiply\n+        self.filters["multiply"] = None
```

### Mutant 1020

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1020.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2741,7 +2741,7 @@\n-        self.filters["add"] = add\n+        self.filters["add"] = None
```

### Mutant 1207

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1207.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2842,7 +2842,7 @@\n-        def hassfunction[**_P, _R](\n+        def hassfunction[*_P, _R](
```

### Mutant 1210

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1210.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2857,7 +2857,7 @@\n-        self.globals["device_entities"] = hassfunction(device_entities)\n+        self.globals["device_entities"] = None
```

### Mutant 1213

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1213.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2858,7 +2858,7 @@\n-        self.filters["device_entities"] = self.globals["device_entities"]\n+        self.filters["device_entities"] = None
```

### Mutant 1342

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1342.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2935,33 +2935,7 @@\n-            hass_globals = [\n-                "closest",\n-                "distance",\n-                "expand",\n-                "is_hidden_entity",\n-                "is_state",\n-                "is_state_attr",
```

### Mutant 1353

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1353.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2962,18 +2962,7 @@\n-            hass_filters = [\n-                "closest",\n-                "expand",\n-                "device_id",\n-                "area_id",\n-                "area_name",\n-                "floor_id",
```

### Mutant 1358

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1358.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -2974,12 +2974,7 @@\n-            hass_tests = [\n-                "has_value",\n-                "is_hidden_entity",\n-                "is_state",\n-                "is_state_attr",\n-            ]\n+            hass_tests = None
```

### Mutant 1394

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1394.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3004,7 +3004,7 @@\n-        self.filters["states"] = self.globals["states"]\n+        self.filters["states"] = None
```

### Mutant 1396

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1396.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3005,7 +3005,7 @@\n-        self.globals["state_translated"] = StateTranslated(hass)\n+        self.globals["state_translated"] = None
```

### Mutant 1399

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1399.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3006,7 +3006,7 @@\n-        self.filters["state_translated"] = self.globals["state_translated"]\n+        self.filters["state_translated"] = None
```

### Mutant 1401

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1401.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3007,7 +3007,7 @@\n-        self.globals["has_value"] = hassfunction(has_value)\n+        self.globals["has_value"] = None
```

### Mutant 1404

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1404.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3008,7 +3008,7 @@\n-        self.filters["has_value"] = self.globals["has_value"]\n+        self.filters["has_value"] = None
```

### Mutant 1406

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1406.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3009,7 +3009,7 @@\n-        self.tests["has_value"] = hassfunction(has_value, pass_eval_context)\n+        self.tests["has_value"] = None
```

### Mutant 1408

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1408.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3010,7 +3010,7 @@\n-        self.globals["utcnow"] = hassfunction(utcnow)\n+        self.globals["utcnow"] = None
```

### Mutant 1410

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1410.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3011,7 +3011,7 @@\n-        self.globals["now"] = hassfunction(now)\n+        self.globals["now"] = None
```

### Mutant 1412

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1412.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3012,7 +3012,7 @@\n-        self.globals["relative_time"] = hassfunction(relative_time)\n+        self.globals["relative_time"] = None
```

### Mutant 1431

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1431.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3025,7 +3025,7 @@\n-        ) or super().is_safe_callable(obj)\n+        ) and super().is_safe_callable(obj)
```

### Mutant 1435

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1435.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3035,7 +3035,7 @@\n-            return True\n+            return False
```

### Mutant 1436

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1436.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3039,7 +3039,6 @@\n-    @overload
```

### Mutant 1437

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1437.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3045,7 +3045,7 @@\n-        raw: Literal[False] = False,\n+        raw: Literal[False] = True,
```

### Mutant 1439

- Class: **T1: value-template rendering/interpreting**
- Diff: `resultados_mutmut/template/boofuzz/seed_1/mutant_diffs/mutant_1439.diff`

```diff
--- ha_source/homeassistant/helpers/template.py\n+++ ha_source/homeassistant/helpers/template.py\n@@ -3049,7 +3049,6 @@\n-    @overload
```

