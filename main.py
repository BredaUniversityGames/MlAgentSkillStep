from GUI import GUI

if __name__ == "__main__":
    gui = GUI(0)
    gui.startRender()



# env_id= "StreetFighterIISpecialChampionEdition-Genesis"
# env = retro.make(env_id, state='2p', players=2)
# obs = env.reset()
# # env = SubprocVecEnv([retro.make(env_id, state='Champion.Level1.RyuVsGuile') for i in range(n_cpus)])
#
# # model = PPO("MlpPolicy", env, verbose=1)
# # # # model = PPO.load("streetFighter-ppo-100k")
# # for i in range(100):
# #  model.learn(total_timesteps=500000)
# #  model.save("streetFighter-ppo-500k")
# model = PPO.load("streetFighter-ppo-500k")
#
# # for i in range(100000):
# #     action, _states = model.predict(obs, deterministic=True)
# #     obs, reward, done, info = env.step(action)
# #     env.render()
# #     if done:
# #       obs = env.reset()
# #
# # env.close()
