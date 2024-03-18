import json
import re
import requests

# Change this field for your language.
language = 'ja_JP'
# Change this field if you want to target different version.
newer_version = '1.20.4'

# Things that have different arguments, different use case, or just removed.
# You can still check how they're changed and maybe adopt them.
skip_list = (
    'chat.type.achievement',
    'commands.ban.failed',
    'commands.ban.success',
    'commands.banip.success',
    'commands.deop.failed',
    'commands.kick.success',
    'commands.message.display.incoming',
    'commands.message.display.outgoing',
    'commands.op.failed',
    'commands.save.failed',
    'commands.scoreboard.players.list.empty',
    'commands.setblock.success',
    'commands.setworldspawn.success',
    'commands.spreadplayers.success.teams',
    'commands.summon.success',
    'commands.whitelist.add.failed',
    'commands.whitelist.list',
    'commands.whitelist.remove.failed',
    'container.minecart',
    'createWorld.customize.flat.addLayer',
    'createWorld.customize.flat.editLayer',
    'death.fell.accident.water',
    'demo.day.6',
    'deathScreen.deleteWorld',
    'deathScreen.hardcoreInfo',
    'deathScreen.leaveServer',
    'entity.EntityHorse.name',
    'entity.Mob.name',
    'entity.Monster.name',
    'entity.PigZombie.name',
    'entity.generic.name',
    'gameMode.changed',
    'gui.achievements',
    'item.bed.name',
    'item.boat.name',
    'item.dyePowder.black.name',
    'item.dyePowder.blue.name',
    'item.dyePowder.brown.name',
    'item.dyePowder.white.name',
    'item.fish.cod.cooked.name',
    'item.fish.cod.raw.name',
    'item.leaves.name',
    'item.monsterPlacer.name',
    'item.record.name',
    'item.ruby.name',
    'itemGroup.brewing',
    'itemGroup.decorations',
    'itemGroup.food',
    'itemGroup.misc',
    'itemGroup.transportation',
    'key.categories.stream',
    'key.streamCommercial',
    'key.streamPauseUnpause',
    'key.streamStartStop',
    'key.streamToggleMic',
    'language.code',
    'mcoServer.title',
    'menu.simulating',
    'menu.switchingLevel',
    'multiplayer.connect',
    'multiplayer.info1',
    'multiplayer.info2',
    'multiplayer.ipinfo',
    'potion.absorption.postfix',
    'potion.blindness.postfix',
    'potion.confusion.postfix',
    'potion.digSlowDown.postfix',
    'potion.digSpeed.postfix',
    'potion.healthBoost.postfix',
    'potion.hunger.postfix',
    'potion.resistance.postfix',
    'potion.saturation.postfix',
    'potion.wither.postfix',
    'selectServer.deleteWarning',
    'selectWorld.allowCommands.info',
    'selectWorld.deleteWarning',
    'selectWorld.mapFeatures.info',
    'tile.anvil.intact.name',
    'tile.bed.name',
    'tile.bed.notValid',
    'tile.button.name',
    'tile.cloth.name',
    'tile.crops.name',
    'tile.leaves.name',
    'tile.lockedchest.name',
    'tile.log.name',
    'tile.mushroom.name',
    'tile.oreRuby.name',
    'tile.pressurePlate.name',
    'tile.redstoneDust.name',
    'tile.sandStone.name',
    'tile.sign.name',
    'tile.stainedGlass.name',
    'tile.stoneSlab.wood.name',
    'tile.stonebricksmooth.name',
    'tile.tallgrass.name',
    'tile.tallgrass.shrub.name',
    'tile.thinStainedGlass.name',
    'tile.wood.name',
    'title.oldgl1',
    'title.oldgl2',
)

item_renames = {
    'appleGold': 'golden_apple',
    'beefCooked': 'cooked_beef',
    'beefRaw': 'beef',
    'bootsChain': 'chainmail_boots',
    'bootsCloth': 'leather_boots',
    'bootsDiamond': 'diamond_boots',
    'bootsGold': 'golden_boots',
    'bootsIron': 'iron_boots',
    'bucketLava': 'lava_bucket',
    'bucketWater': 'water_bucket',
    'carrotGolden': 'golden_carrot',
    'carrots': 'carrot',
    'chestplateChain': 'chainmail_chestplate',
    'chestplateCloth': 'leather_chestplate',
    'chestplateDiamond': 'diamond_chestplate',
    'chestplateGold': 'golden_chestplate',
    'chestplateIron': 'iron_chestplate',
    'chickenCooked': 'cooked_chicken',
    'chickenRaw': 'chicken',
    'clay': 'clay_ball',
    'dyePowder.cyan': 'cyan_dye',
    'dyePowder.gray': 'gray_dye',
    'dyePowder.green': 'green_dye',
    'dyePowder.lightBlue': 'light_blue_dye',
    'dyePowder.lime': 'lime_dye',
    'dyePowder.magenta': 'magenta_dye',
    'dyePowder.orange': 'orange_dye',
    'dyePowder.pink': 'pink_dye',
    'dyePowder.purple': 'purple_dye',
    'dyePowder.red': 'red_dye',
    'dyePowder.silver': 'light_gray_dye',
    'dyePowder.yellow': 'yellow_dye',
    'emptyMap': 'map',
    'emptyPotion': 'potion.effect.water',
    'expBottle': 'experience_bottle',
    'eyeOfEnder': 'ender_eye',
    'fireball': 'fire_charge',
    'fireworks': 'firework_rocket',
    'fireworksCharge': 'firework_star',
    'fish.pufferfish.raw': 'pufferfish',
    'fish.salmon.cooked': 'cooked_salmon',
    'fish.salmon.raw': 'salmon',
    'frame': 'item_frame',
    'hatchetDiamond': 'diamond_axe',
    'hatchetGold': 'golden_axe',
    'hatchetIron': 'iron_axe',
    'hatchetStone': 'stone_axe',
    'hatchetWood': 'wooden_axe',
    'helmetChain': 'chainmail_helmet',
    'helmetCloth': 'leather_helmet',
    'helmetDiamond': 'diamond_helmet',
    'helmetGold': 'golden_helmet',
    'helmetIron': 'iron_helmet',
    'hoeDiamond': 'diamond_hoe',
    'hoeGold': 'golden_hoe',
    'hoeIron': 'iron_hoe',
    'hoeStone': 'stone_hoe',
    'hoeWood': 'wooden_hoe',
    'horsearmordiamond': 'diamond_horse_armor',
    'horsearmorgold': 'golden_horse_armor',
    'horsearmormetal': 'iron_horse_armor',
    'ingotGold': 'gold_ingot',
    'ingotIron': 'iron_ingot',
    'leash': 'lead',
    'leggingsChain': 'chainmail_leggings',
    'leggingsCloth': 'leather_leggings',
    'leggingsDiamond': 'diamond_leggings',
    'leggingsGold': 'golden_leggings',
    'leggingsIron': 'iron_leggings',
    'map': 'filled_map',
    'melon': 'melon_slice',
    'milk': 'milk_bucket',
    'minecartChest': 'chest_minecart',
    'minecartCommandBlock': 'command_block_minecart',
    'minecartFurnace': 'furnace_minecart',
    'minecartHopper': 'hopper_minecart',
    'minecartTnt': 'tnt_minecart',
    'netherStalkSeeds': 'nether_wart',
    'netherbrick': 'nether_brick',
    'netherquartz': 'quartz',
    'pickaxeDiamond': 'diamond_pickaxe',
    'pickaxeGold': 'golden_pickaxe',
    'pickaxeIron': 'iron_pickaxe',
    'pickaxeStone': 'stone_pickaxe',
    'pickaxeWood': 'wooden_pickaxe',
    'porkchopCooked': 'cooked_porkchop',
    'porkchopRaw': 'porkchop',
    'potatoBaked': 'baked_potato',
    'potatoPoisonous': 'poisonous_potato',
    'seeds': 'wheat_seeds',
    'seeds_melon': 'melon_seeds',
    'seeds_pumpkin': 'pumpkin_seeds',
    'shovelDiamond': 'diamond_shovel',
    'shovelGold': 'golden_shovel',
    'shovelIron': 'iron_shovel',
    'shovelStone': 'stone_shovel',
    'shovelWood': 'wooden_shovel',
    'slimeball': 'slime_ball',
    'speckledMelon': 'glistering_melon_slice',
    'sulphur': 'gunpowder',
    'swordDiamond': 'diamond_sword',
    'swordGold': 'golden_sword',
    'swordIron': 'iron_sword',
    'swordStone': 'stone_sword',
    'swordWood': 'wooden_sword',
    'writingBook': 'writable_book',
    'yellowDust': 'glowstone_dust',
}

block_renames = {
    'anvil.slightlyDamaged': 'chipped_anvil',
    'anvil.veryDamaged': 'damaged_anvil',
    'blockCoal': 'coal_block',
    'blockDiamond': 'diamond_block',
    'blockEmerald': 'emerald_block',
    'blockGold': 'gold_block',
    'blockIron': 'iron_block',
    'blockLapis': 'lapis_block',
    'blockRedstone': 'redstone_block',
    'brick': 'bricks',
    'chestTrap': 'trapped_chest',
    'clayHardened': 'terracotta',
    'clayHardenedStained.black': 'black_terracotta',
    'clayHardenedStained.blue': 'blue_terracotta',
    'clayHardenedStained.brown': 'brown_terracotta',
    'clayHardenedStained.cyan': 'cyan_terracotta',
    'clayHardenedStained.gray': 'gray_terracotta',
    'clayHardenedStained.green': 'green_terracotta',
    'clayHardenedStained.lightBlue': 'light_blue_terracotta',
    'clayHardenedStained.lime': 'lime_terracotta',
    'clayHardenedStained.magenta': 'magenta_terracotta',
    'clayHardenedStained.orange': 'orange_terracotta',
    'clayHardenedStained.pink': 'pink_terracotta',
    'clayHardenedStained.purple': 'purple_terracotta',
    'clayHardenedStained.red': 'red_terracotta',
    'clayHardenedStained.silver': 'light_gray_terracotta',
    'clayHardenedStained.white': 'white_terracotta',
    'clayHardenedStained.yellow': 'yellow_terracotta',
    'cloth.black': 'black_wool',
    'cloth.blue': 'blue_wool',
    'cloth.brown': 'brown_wool',
    'cloth.cyan': 'cyan_wool',
    'cloth.gray': 'gray_wool',
    'cloth.green': 'green_wool',
    'cloth.lightBlue': 'light_blue_wool',
    'cloth.lime': 'lime_wool',
    'cloth.magenta': 'magenta_wool',
    'cloth.orange': 'orange_wool',
    'cloth.pink': 'pink_wool',
    'cloth.purple': 'purple_wool',
    'cloth.red': 'red_wool',
    'cloth.silver': 'light_gray_wool',
    'cloth.white': 'white_wool',
    'cloth.yellow': 'yellow_wool',
    'cobbleWall.mossy': 'mossy_cobblestone_wall',
    'cobbleWall.normal': 'cobblestone_wall',
    'deadbush': 'dead_bush',
    'dirt.default': 'dirt',
    'dirt.podzol': 'podzol',
    'doorIron': 'iron_door',
    'doorWood': 'oak_door',
    'doublePlant.fern': 'large_fern',
    'doublePlant.grass': 'tall_grass',
    'doublePlant.paeonia': 'peony',
    'doublePlant.rose': 'rose_bush',
    'doublePlant.sunflower': 'sunflower',
    'doublePlant.syringa': 'lilac',
    'enchantmentTable': 'enchanting_table',
    'fence': 'oak_fence',
    'fenceGate': 'oak_fence_gate',
    'fenceIron': 'iron_bars',
    'flower1.dandelion': 'dandelion',
    'flower2.allium': 'allium',
    'flower2.blueOrchid': 'blue_orchid',
    'flower2.houstonia': 'azure_bluet',
    'flower2.oxeyeDaisy': 'oxeye_daisy',
    'flower2.poppy': 'poppy',
    'flower2.tulipOrange': 'orange_tulip',
    'flower2.tulipPink': 'pink_tulip',
    'flower2.tulipRed': 'red_tulip',
    'flower2.tulipWhite': 'white_tulip',
    'goldenRail': 'powered_rail',
    'grass': 'grass_block',
    'hellrock': 'netherrack',
    'hellsand': 'soul_sand',
    'icePacked': 'packed_ice',
    'leaves.acacia': 'acacia_leaves',
    'leaves.big_oak': 'dark_oak_leaves',
    'leaves.birch': 'birch_leaves',
    'leaves.jungle': 'jungle_leaves',
    'leaves.oak': 'oak_leaves',
    'leaves.spruce': 'spruce_leaves',
    'lightgem': 'glowstone',
    'litpumpkin': 'jack_o_lantern',
    'log.acacia': 'acacia_log',
    'log.big_oak': 'dark_oak_log',
    'log.birch': 'birch_log',
    'log.jungle': 'jungle_log',
    'log.oak': 'oak_log',
    'log.spruce': 'spruce_log',
    'mobSpawner': 'spawner',
    'monsterStoneEgg.brick': 'infested_stone_bricks',
    'monsterStoneEgg.chiseledbrick': 'infested_chiseled_stone_bricks',
    'monsterStoneEgg.cobble': 'infested_cobblestone',
    'monsterStoneEgg.crackedbrick': 'infested_cracked_stone_bricks',
    'monsterStoneEgg.mossybrick': 'infested_mossy_stone_bricks',
    'monsterStoneEgg.stone': 'infested_stone',
    'musicBlock': 'note_block',
    'mycel': 'mycelium',
    'netherBrick': 'nether_bricks',
    'netherFence': 'nether_brick_fence',
    'netherStalk': 'nether_wart',
    'netherquartz': 'nether_quartz_ore',
    'notGate': 'redstone_torch',
    'oreCoal': 'coal_ore',
    'oreDiamond': 'diamond_ore',
    'oreEmerald': 'emerald_ore',
    'oreGold': 'gold_ore',
    'oreIron': 'iron_ore',
    'oreLapis': 'lapis_ore',
    'oreRedstone': 'redstone_ore',
    'pistonBase': 'piston',
    'pistonStickyBase': 'sticky_piston',
    'portal': 'nether_portal',
    'quartzBlock.chiseled': 'chiseled_quartz_block',
    'quartzBlock.default': 'quartz_block',
    'quartzBlock.lines': 'quartz_pillar',
    'redstoneLight': 'redstone_lamp',
    'reeds': 'sugar_cane',
    'sand.default': 'sand',
    'sand.red': 'red_sand',
    'sandStone.chiseled': 'chiseled_sandstone',
    'sandStone.default': 'sandstone',
    'sandStone.smooth': 'cut_sandstone',
    'sapling.acacia': 'acacia_sapling',
    'sapling.birch': 'birch_sapling',
    'sapling.jungle': 'jungle_sapling',
    'sapling.oak': 'oak_sapling',
    'sapling.roofed_oak': 'dark_oak_sapling',
    'sapling.spruce': 'spruce_sapling',
    'stainedGlass.black': 'black_stained_glass',
    'stainedGlass.blue': 'blue_stained_glass',
    'stainedGlass.brown': 'brown_stained_glass',
    'stainedGlass.cyan': 'cyan_stained_glass',
    'stainedGlass.gray': 'gray_stained_glass',
    'stainedGlass.green': 'green_stained_glass',
    'stainedGlass.lightBlue': 'light_blue_stained_glass',
    'stainedGlass.lime': 'lime_stained_glass',
    'stainedGlass.magenta': 'magenta_stained_glass',
    'stainedGlass.orange': 'orange_stained_glass',
    'stainedGlass.pink': 'pink_stained_glass',
    'stainedGlass.purple': 'purple_stained_glass',
    'stainedGlass.red': 'red_stained_glass',
    'stainedGlass.silver': 'light_gray_stained_glass',
    'stainedGlass.white': 'white_stained_glass',
    'stainedGlass.yellow': 'yellow_stained_glass',
    'stairsBrick': 'brick_stairs',
    'stairsNetherBrick': 'nether_brick_stairs',
    'stairsQuartz': 'quartz_stairs',
    'stairsSandStone': 'sandstone_stairs',
    'stairsStone': 'cobblestone_stairs',
    'stairsStoneBrickSmooth': 'stone_brick_stairs',
    'stairsWood': 'oak_stairs',
    'stairsWoodAcacia': 'acacia_stairs',
    'stairsWoodBirch': 'birch_stairs',
    'stairsWoodDarkOak': 'dark_oak_stairs',
    'stairsWoodJungle': 'jungle_stairs',
    'stairsWoodSpruce': 'spruce_stairs',
    'stoneMoss': 'mossy_cobblestone',
    'stoneSlab.brick': 'brick_slab',
    'stoneSlab.cobble': 'cobblestone_slab',
    'stoneSlab.netherBrick': 'nether_brick_slab',
    'stoneSlab.quartz': 'quartz_slab',
    'stoneSlab.sand': 'sandstone_slab',
    'stoneSlab.smoothStoneBrick': 'stone_brick_slab',
    'stoneSlab.stone': 'stone_slab',
    'stonebrick': 'cobblestone',
    'stonebricksmooth.chiseled': 'chiseled_stone_bricks',
    'stonebricksmooth.cracked': 'cracked_stone_bricks',
    'stonebricksmooth.default': 'stone_bricks',
    'stonebricksmooth.mossy': 'mossy_stone_bricks',
    'tallgrass.fern': 'fern',
    'tallgrass.grass': 'short_grass',
    'thinGlass': 'glass_pane',
    'thinStainedGlass.black': 'black_stained_glass_pane',
    'thinStainedGlass.blue': 'blue_stained_glass_pane',
    'thinStainedGlass.brown': 'brown_stained_glass_pane',
    'thinStainedGlass.cyan': 'cyan_stained_glass_pane',
    'thinStainedGlass.gray': 'gray_stained_glass_pane',
    'thinStainedGlass.green': 'green_stained_glass_pane',
    'thinStainedGlass.lightBlue': 'light_blue_stained_glass_pane',
    'thinStainedGlass.lime': 'lime_stained_glass_pane',
    'thinStainedGlass.magenta': 'magenta_stained_glass_pane',
    'thinStainedGlass.orange': 'orange_stained_glass_pane',
    'thinStainedGlass.pink': 'pink_stained_glass_pane',
    'thinStainedGlass.purple': 'purple_stained_glass_pane',
    'thinStainedGlass.red': 'red_stained_glass_pane',
    'thinStainedGlass.silver': 'light_gray_stained_glass_pane',
    'thinStainedGlass.white': 'white_stained_glass_pane',
    'thinStainedGlass.yellow': 'yellow_stained_glass_pane',
    'trapdoor': 'oak_trapdoor',
    'tripWire': 'tripwire',
    'tripWireSource': 'tripwire_hook',
    'waterlily': 'lily_pad',
    'web': 'cobweb',
    'weightedPlate_heavy': 'heavy_weighted_pressure_plate',
    'weightedPlate_light': 'light_weighted_pressure_plate',
    'whiteStone': 'end_stone',
    'wood.acacia': 'acacia_planks',
    'wood.big_oak': 'dark_oak_planks',
    'wood.birch': 'birch_planks',
    'wood.jungle': 'jungle_planks',
    'wood.oak': 'oak_planks',
    'wood.spruce': 'spruce_planks',
    'woodSlab.acacia': 'acacia_slab',
    'woodSlab.big_oak': 'dark_oak_slab',
    'woodSlab.birch': 'birch_slab',
    'woodSlab.jungle': 'jungle_slab',
    'woodSlab.oak': 'oak_slab',
    'woodSlab.spruce': 'spruce_slab',
    'woolCarpet.black': 'black_carpet',
    'woolCarpet.blue': 'blue_carpet',
    'woolCarpet.brown': 'brown_carpet',
    'woolCarpet.cyan': 'cyan_carpet',
    'woolCarpet.gray': 'gray_carpet',
    'woolCarpet.green': 'green_carpet',
    'woolCarpet.lightBlue': 'light_blue_carpet',
    'woolCarpet.lime': 'lime_carpet',
    'woolCarpet.magenta': 'magenta_carpet',
    'woolCarpet.orange': 'orange_carpet',
    'woolCarpet.pink': 'pink_carpet',
    'woolCarpet.purple': 'purple_carpet',
    'woolCarpet.red': 'red_carpet',
    'woolCarpet.silver': 'light_gray_carpet',
    'woolCarpet.white': 'white_carpet',
    'woolCarpet.yellow': 'yellow_carpet',
    'workbench': 'crafting_table',
}

# Things that use block name instead of item name.
item_block_renames = {
    'cake': 'cake',
    'comparator': 'comparator',
    'diode': 'repeater',
    'doorIron': 'iron_door',
    'reeds': 'sugar_cane',
    'skull.char': 'player_head',
    'skull.creeper': 'creeper_head',
    'skull.player': 'player_head.named',
    'skull.skeleton': 'skeleton_skull',
    'skull.wither': 'wither_skeleton_skull',
    'skull.zombie': 'zombie_head',
}

other_renames = {
    'enchantment.arrowDamage': 'enchantment.minecraft.power',
    'enchantment.arrowFire': 'enchantment.minecraft.flame',
    'enchantment.arrowInfinite': 'enchantment.minecraft.infinity',
    'enchantment.arrowKnockback': 'enchantment.minecraft.punch',
    'enchantment.damage.all': 'enchantment.minecraft.sharpness',
    'enchantment.damage.arthropods': 'enchantment.minecraft.bane_of_arthropods',
    'enchantment.damage.undead': 'enchantment.minecraft.smite',
    'enchantment.digging': 'enchantment.minecraft.efficiency',
    'enchantment.durability': 'enchantment.minecraft.unbreaking',
    'enchantment.fire': 'enchantment.minecraft.fire_aspect',
    'enchantment.fishingSpeed': 'enchantment.minecraft.lure',
    'enchantment.knockback': 'enchantment.minecraft.knockback',
    'enchantment.lootBonus': 'enchantment.minecraft.looting',
    'enchantment.lootBonusDigger': 'enchantment.minecraft.fortune',
    'enchantment.lootBonusFishing': 'enchantment.minecraft.luck_of_the_sea',
    'enchantment.oxygen': 'enchantment.minecraft.respiration',
    'enchantment.protect.all': 'enchantment.minecraft.protection',
    'enchantment.protect.explosion': 'enchantment.minecraft.blast_protection',
    'enchantment.protect.fall': 'enchantment.minecraft.feather_falling',
    'enchantment.protect.fire': 'enchantment.minecraft.fire_protection',
    'enchantment.protect.projectile': 'enchantment.minecraft.projectile_protection',
    'enchantment.thorns': 'enchantment.minecraft.thorns',
    'enchantment.untouching': 'enchantment.minecraft.silk_touch',
    'enchantment.waterWorker': 'enchantment.minecraft.aqua_affinity',
    'entity.FallingSand.name': 'entity.minecraft.falling_block',
    'entity.LavaSlime.name': 'entity.minecraft.magma_cube',
    'entity.MushroomCow.name': 'entity.minecraft.mooshroom',
    'entity.Ozelot.name': 'entity.minecraft.ocelot',
    'entity.PrimedTnt.name': 'entity.minecraft.tnt',
    'entity.SnowMan.name': 'entity.minecraft.snow_golem',
    'entity.VillagerGolem.name': 'entity.minecraft.iron_golem',
    'entity.WitherBoss.name': 'entity.minecraft.wither',
    'entity.XPOrb.name': 'entity.minecraft.experience_orb',
    'entity.skeletonhorse.name': 'entity.minecraft.skeleton_horse',
    'entity.zombiehorse.name': 'entity.minecraft.zombie_horse',
    'generator.amplified': 'generator.minecraft.amplified',
    'generator.amplified.info': 'generator.minecraft.amplified.info',
    'generator.default': 'generator.minecraft.normal',
    'generator.flat': 'generator.minecraft.flat',
    'generator.largeBiomes': 'generator.minecraft.large_biomes',
    'item.doorWood.name': 'block.minecraft.oak_door',
    'item.fireworks.flight': 'item.minecraft.firework_rocket.flight',
    'item.fireworksCharge.black': 'item.minecraft.firework_star.black',
    'item.fireworksCharge.blue': 'item.minecraft.firework_star.blue',
    'item.fireworksCharge.brown': 'item.minecraft.firework_star.brown',
    'item.fireworksCharge.customColor': 'item.minecraft.firework_star.custom_color',
    'item.fireworksCharge.cyan': 'item.minecraft.firework_star.cyan',
    'item.fireworksCharge.fadeTo': 'item.minecraft.firework_star.fade_to',
    'item.fireworksCharge.flicker': 'item.minecraft.firework_star.flicker',
    'item.fireworksCharge.gray': 'item.minecraft.firework_star.gray',
    'item.fireworksCharge.green': 'item.minecraft.firework_star.green',
    'item.fireworksCharge.lightBlue': 'item.minecraft.firework_star.light_blue',
    'item.fireworksCharge.lime': 'item.minecraft.firework_star.lime',
    'item.fireworksCharge.magenta': 'item.minecraft.firework_star.magenta',
    'item.fireworksCharge.orange': 'item.minecraft.firework_star.orange',
    'item.fireworksCharge.pink': 'item.minecraft.firework_star.pink',
    'item.fireworksCharge.purple': 'item.minecraft.firework_star.purple',
    'item.fireworksCharge.red': 'item.minecraft.firework_star.red',
    'item.fireworksCharge.silver': 'item.minecraft.firework_star.light_gray',
    'item.fireworksCharge.trail': 'item.minecraft.firework_star.trail',
    'item.fireworksCharge.type': 'item.minecraft.firework_star.shape',
    'item.fireworksCharge.type.0': 'item.minecraft.firework_star.shape.small_ball',
    'item.fireworksCharge.type.1': 'item.minecraft.firework_star.shape.large_ball',
    'item.fireworksCharge.type.2': 'item.minecraft.firework_star.shape.star',
    'item.fireworksCharge.type.3': 'item.minecraft.firework_star.shape.creeper',
    'item.fireworksCharge.type.4': 'item.minecraft.firework_star.shape.burst',
    'item.fireworksCharge.white': 'item.minecraft.firework_star.white',
    'item.fireworksCharge.yellow': 'item.minecraft.firework_star.yellow',
    'item.fish.clownfish.raw.name': 'entity.minecraft.tropical_fish.predefined.5',
    'item.record.11.desc': 'item.minecraft.music_disc_11.desc',
    'item.record.13.desc': 'item.minecraft.music_disc_13.desc',
    'item.record.blocks.desc': 'item.minecraft.music_disc_blocks.desc',
    'item.record.cat.desc': 'item.minecraft.music_disc_cat.desc',
    'item.record.chirp.desc': 'item.minecraft.music_disc_chirp.desc',
    'item.record.far.desc': 'item.minecraft.music_disc_far.desc',
    'item.record.mall.desc': 'item.minecraft.music_disc_mall.desc',
    'item.record.mellohi.desc': 'item.minecraft.music_disc_mellohi.desc',
    'item.record.stal.desc': 'item.minecraft.music_disc_stal.desc',
    'item.record.strad.desc': 'item.minecraft.music_disc_strad.desc',
    'item.record.wait.desc': 'item.minecraft.music_disc_wait.desc',
    'item.record.ward.desc': 'item.minecraft.music_disc_ward.desc',
    'itemGroup.materials': 'itemGroup.ingredients',
    'key.mouseButton': 'key.mouse',
    'potion.effects.whenDrank': 'potion.whenDrank',
    'potion.confusion': 'effect.minecraft.nausea',
    'potion.damageBoost': 'effect.minecraft.strength',
    'potion.damageBoost.postfix': 'item.minecraft.potion.effect.strength',
    'potion.digSlowDown': 'effect.minecraft.mining_fatigue',
    'potion.digSpeed': 'effect.minecraft.haste',
    'potion.empty': 'effect.none',
    'potion.harm': 'effect.minecraft.instant_damage',
    'potion.harm.postfix': 'item.minecraft.potion.effect.harming',
    'potion.heal': 'effect.minecraft.instant_health',
    'potion.heal.postfix': 'item.minecraft.potion.effect.healing',
    'potion.jump': 'effect.minecraft.jump_boost',
    'potion.jump.postfix': 'item.minecraft.potion.effect.leaping',
    'potion.moveSlowdown': 'effect.minecraft.slowness',
    'potion.moveSlowdown.postfix': 'item.minecraft.potion.effect.slowness',
    'potion.moveSpeed': 'effect.minecraft.speed',
    'potion.moveSpeed.postfix': 'item.minecraft.potion.effect.swiftness',
    'potion.potency.1': 'potion.potency.1',
    'potion.potency.2': 'potion.potency.2',
    'potion.potency.3': 'potion.potency.3',
    'tile.beacon.primary': 'block.minecraft.beacon.primary',
    'tile.beacon.secondary': 'block.minecraft.beacon.secondary',
    'tile.bed.noSleep': 'block.minecraft.bed.no_sleep',
    'tile.bed.notSafe': 'block.minecraft.bed.not_safe',
    'tile.bed.occupied': 'block.minecraft.bed.occupied',
    'resourcePack.available.title': 'pack.available.title',
    'resourcePack.folderInfo': 'pack.folderInfo',
    'resourcePack.openFolder': 'pack.openFolder',
    'resourcePack.selected.title': 'pack.selected.title',
}

def main() -> None:
    updated = {}

    newer = json.loads(requests.get(f'https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/{newer_version}/assets/minecraft/lang/{language.lower()}.json').content)
    for line in requests.get(f'https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.7.10/assets/minecraft/lang/{language}.lang').content.decode().split('\n'):
        line = line.strip()
        split = line.split('=')
        if (len(split) < 2):
            continue
        if (len(split) > 2):
            raise RuntimeError(f'Unexpected string: {line}')
        key = split[0]
        value = split[1]
        if key.startswith('achievement.') or 'stream' in key or key.startswith('potion.prefix.') or re.match(r'^commands\..+\.usage$', key):
            continue
        if key in skip_list:
            continue
        
        newer_key = rename_key(key)
        if newer_key in newer and value != newer[newer_key]:
            updated[key] = newer[newer_key]
        if newer_key not in newer:
            # This prints all the keys unused
            # print(newer_key)
            pass

    with open(f'{language}.lang', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(map(lambda item: f'{item[0]}={item[1]}', updated.items())))

def rename_key(key: str) -> str:
    if key in other_renames:
        return other_renames[key]

    m = re.match(r'^item\.(.+)\.name$', key)
    if m:
        item_name = m.group(1)
        if item_name in item_block_renames:
            return f'block.minecraft.{item_block_renames[item_name]}'
        if item_name in item_renames:
            item_name = item_renames[item_name]
        return f'item.minecraft.{to_snake_case(item_name)}'
    
    m = re.match(r'^attribute\.name\.(.+)$', key)
    if m:
        block_name = m.group(1)
        return f'attribute.name.{to_snake_case(block_name)}'

    m = re.match(r'^tile\.(.+)\.name$', key)
    if m:
        block_name = m.group(1)
        if block_name in block_renames:
            block_name = block_renames[block_name]
        return f'block.minecraft.{to_snake_case(block_name)}'
    
    m = re.match(r'^entity\.(.+)\.name$', key)
    if m:
        entity_name = m.group(1)
        return f'entity.minecraft.{to_snake_case(entity_name)}'
    
    m = re.match(r'^stat\.(.+)$', key)
    if m:
        stat_name = m.group(1)
        return f'stat.minecraft.{to_snake_case(stat_name)}'
    
    m = re.match(r'^potion\.(.+)\.postfix$', key)
    if m:
        potion_name = m.group(1)
        return f'item.minecraft.potion.effect.{to_snake_case(potion_name)}'
    else:
        m = re.match(r'^potion\.(.+)$', key)
        if m:
            potion_name = m.group(1)
            return f'effect.minecraft.{to_snake_case(potion_name)}'
    
    return key

def to_snake_case(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

if __name__ == '__main__':
    main()
