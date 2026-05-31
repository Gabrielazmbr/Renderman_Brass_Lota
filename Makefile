RMANTREE=/Applications/Pixar/RenderManProServer-27.2
PYTHON=/usr/local/bin/python3.11
SCRIPT=main.py
RIB=output/main.rib
OUTPUT=output/render.exr

RMAN_ENV=RMANTREE=$(RMANTREE) \
         PATH=$(RMANTREE)/bin:$$PATH \
         PYTHONPATH=$(RMANTREE)/bin \
         RMAN_SHADERPATH=./shaders \
         RMAN_TEXTUREPATH=./textures \
         RMAN_HDRIPATH=./hdri

RUN=arch -x86_64

compile_shaders:
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone1_skin.osl -o shaders/zone1_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone2_skin.osl -o shaders/zone2_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone3_skin.osl -o shaders/zone3_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone4_skin.osl -o shaders/zone4_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone5_skin.osl -o shaders/zone5_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/zone6_skin.osl -o shaders/zone6_skin.oso
	$(RMAN_ENV) $(RUN) $(RMANTREE)/bin/oslc shaders/ground_wood.osl -o shaders/ground_wood.oso

generate: compile_shaders
	$(RMAN_ENV) $(RUN) $(PYTHON) $(SCRIPT)

render:
	$(RMAN_ENV) $(RUN) prman -progress $(RIB)

both: generate render

view:
	$(RUN) $(RMANTREE)/bin/it.app/Contents/MacOS/it $(OUTPUT)

clean:
	rm -f output/*.rib output/*.exr

.PHONY: generate render both view clean compile_shaders
