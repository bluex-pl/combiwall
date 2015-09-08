CombiWall
=========

Simple program to combine multiple images into a single wallpaper. 
It could be used in multi-monitor setups on systems that don't support
the configuration of per-screen wallpaper.

Usage
-----

* Create `config.yml` like this::

    ## Configuration variables ##
    out_path: ./wallpapers
    name_pattern: wallpaper-{:02d}.png
    start: 1 # name indexing start

    ## Workspaces configuration ##
    workspaces:
      - name: ws-1
        screens:
          - name: s-1
            x: 0
            y: 0
            w: 1080
            h: 1920
          - name: s-2
            x: left s-1
            y: 343 #center s-1
            w: 1920
            h: 1200

    ## Images to combine ##
    combine:
      - images:
          s-1: ia_by_shirokujaku-d7rs31x.jpg
          s-2: dream_within_a_dream_by_nanomortis-d79doyy.png
        workspace: ws-1
      - images:
          s-1: commission_for_ifabulicious_by_inma-d7vekpc.jpg
          s-2: no_longer_the_lost_by_nanomortis-d6z2gso.png
        workspace: ws-1

* Run `python3 cw.py`
* Select new image as wallpaper in span / extend mode.

